from django.shortcuts import render
import datetime
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.paginator import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import calendar



def month_name(month_number):
    return calendar.month_name[month_number]

@login_required(login_url='/findr/login')
def index(request):
    usertype = request.session.get('usertype', None)
    time_loop = range(0,12)
    today = datetime.datetime.now()
    dates=[13]
    for i in time_loop:
        date = today + datetime.timedelta(days=i)
        dates.append(date) 

    return render(request, 'findr/index.html', {'usertype':usertype, 'time_loop':time_loop, 'dates':dates})
    
   


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/findr/login')



def admin(request):
    # if request.method == 'GET':

    #     return render(request, 'findr/searchtest.html')
    #     pass
    return render(request, 'findr/index.html', {'usertype':"admin"})

# def index(request):
#     retdict = {'articles': Article.objects.all(),}
#     return render_to_response('findr/index.html', retdict, context_instance=RequestContext(request))

def welcome(request):
    return render(request, 'findr/welcome.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        
        return render(request, 'findr/activate_redirect.html')

        return 
    else:
        return HttpResponse('Activation link is invalid!')

def register(request):
    # Like before, get the request's context.
##    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.is_active = False
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True


            current_site = get_current_site(request)
            message = render_to_string("findr/acc_active_email.html", {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

        else:
            print (user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'findr/register.htm', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    # Like before, obtain the context for the user's request.
    # context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']


        USERTYPES = (
        ('1', 'Student'),
        ('2', 'Tourist'),
        ('3', 'Businessman'),
        )
        
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        userAuth = authenticate(username=username, password=password)
        
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if userAuth:
            # Is the account active? It could have been disabled.
            if userAuth.is_active:
                # If the account is valid and active, we can now check user types.
                # We'll send the user back to the homepage.
                
                # Gets username from the user table in the database
                dbuser = User.objects.get(username=username)

                # Check whether user type is a student
                try:
                    student = UserProfile.objects.get(usertype='1', user=dbuser)
                except ObjectDoesNotExist:
                    student = None

                # Check whether user type is a tourist
                try:
                    tourist = UserProfile.objects.get(usertype='2', user=dbuser)
                except ObjectDoesNotExist:
                    tourist = None

                # Check whether user type is a businessman
                try:
                    businessman = UserProfile.objects.get(usertype='3', user=dbuser)
                except ObjectDoesNotExist:
                    businessman = None

                # Check whether user is an admin
                # If user is an admin, redirects admin to admin home page
                if userAuth.is_superuser:
                    login(request, userAuth)
                    request.session['usertype'] = "admin"
                    request.session.modified = True
                    print(request.session.get('usertype'))
                    return HttpResponseRedirect('/findr/index')

                # Check whether user is a student by using "if is not None"
                # If user is a student, redirects user to student home page 
                if student is not None:
                    login(request, userAuth)
                    request.session['usertype'] = "student"
                    request.session.modified = True
                    print(request.session.get('usertype'))
                    return HttpResponseRedirect('/findr/index')

                # Check whether user is a tourist by using "if is not None"
                # If user is a tourist, redirects user to tourist home page 
                elif tourist is not None:
                    login(request, userAuth)
                    request.session['usertype'] = "tourist"
                    request.session.modified = True
                    print(request.session.get('usertype'))
                    return HttpResponseRedirect('/findr/index')

                # Check whether user is a businessman by using "if is not None"
                # If user is a businessman, redirects user to businessman home page 
                elif businessman is not None:
                    login(request, userAuth)
                    request.session['usertype'] = "businessman"
                    request.session.modified = True
                    print(request.session.get('usertype'))
                    return HttpResponseRedirect('/findr/index')
                
                # If there user exists and is not a student, tourist or businessman
                # Output the message saying account has been disabled
                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Your Findr account is disabled.")
                
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Findr account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            #"Invalid login details supplied."
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    elif request.session.get('usertype', None) is not None:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return HttpResponseRedirect('/findr/index')
    else:

        return render(request, "findr/login.html")


@login_required(login_url='/findr/login')
def searchtest(request):

    if request.method == "POST":
        search_target = request.POST['search']

        result = CityInfoDetail.objects.filter(name__iexact=search_target)
        
        return render(request, "findr/resultspage.html", {'CityInfoDetails':results})
    else:
        return render(request, "findr/searchtest.html", {})





@login_required(login_url='/findr/login')
def category(request, category):

# many to many filter. cityinfodetail info with citycategory!! important!
    result_list = CityInfoDetail.objects.filter(category__name__iexact=category)
    paginator = Paginator(result_list, 4)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:

        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, "findr/resultspage.html", {'results':results, 'category':category})

@login_required(login_url='/findr/login')
def itempage(request):

    itemtarget = request.GET.get('target')

    targetGoogleMap = CityInfoDetail.objects.filter(name__exact=itemtarget)

    return render(request, 'findr/itempage.html', {'googlemap':targetGoogleMap})

def search(request):
    if request.method == "POST":
        search_target = request.POST['search']
        request.session['search_target'] = search_target
        request.modified = True
        
        result_list = CityInfoDetail.objects.filter(name__icontains=search_target)
        paginator = Paginator(result_list, 4)
        
        page = request.GET.get('page')

        try:
            results = paginator.page(page)
        except PageNotAnInteger:

            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return render(request, "findr/resultspage.html", {'results':results})

    elif request.session.get('search_target', None) is not None:
        search_target = request.session.get('search_target', None)
        result_list = CityInfoDetail.objects.filter(name__icontains=search_target)
        paginator = Paginator(result_list, 4)
        page = request.GET.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:

            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return render(request, "findr/resultspage.html", {'results':results})
    else:
        return render(request, "findr/index.html", {})