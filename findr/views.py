from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from .models import *
from django.core.paginator import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def index(request):
    # if request.method == 'GET':

    #     return render(request, 'findr/searchtest.html')
    #     pass
    return render(request, 'findr/index.html')

# def index(request):
#     retdict = {'articles': Article.objects.all(),}
#     return render_to_response('findr/index.html', retdict, context_instance=RequestContext(request))

def welcome(request):
    return render(request, 'findr/welcome.html')


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

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
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

##        class SettingsBackend(object):
##            def has_perm(self, user_obj, perm, obj=None):
##                if user_obj.username == settings.ADMIN_LOGIN:
##                    return True
##                else:
##                    return False
##
##            def typeAuth(username=None, password=None, usertype=None):
##                login_valid = (settings.ADMIN_LOGIN == username)
##                pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
##                type_valid = (settings.ADMIN_USERTYPE == usertype)
##                if login_valid and pwd_valid and type_valid:
##                    try:
##                        user = User.objects.get(username=username)
##                    except User.DoesNotExist:
##                        # Create a new user. Note that we can set password
##                        # to anything, because it won't be checked; the password
##                        # from settings.py will.
##                        user = User(username=username, password='get from settings.py')
##                        user.is_staff = True
##                        user.is_superuser = True
##                        user.save()
##                    return user
##                return None
##
##            def get_user(self, user_id):
##                try:
##                   return User.objects.get(pk=user_id)
##                except User.DoesNotExist:
##                   return None

        USERTYPES = (
        ('1', 'Student'),
        ('2', 'Tourist'),
        ('3', 'Businessman'),
        )
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        userAuth = authenticate(username=username, password=password)
        test = User.objects.get(username=username)

##        student = authenticate(username=username, password=password, usertype='Student')
##        tourist = authenticate(username=username, password=password, usertype='Tourist')
##        businessman = authenticate(username=username, password=password, usertype='Businessman')
        
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if userAuth:
            # Is the account active? It could have been disabled.
            if userAuth.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.

                #UserProfile.objects.all().values_list('usertype', flat=True)
                try:
                    student = UserProfile.objects.get(usertype='1', user=test)
                except ObjectDoesNotExist:
                    student = None

                try:
                    tourist = UserProfile.objects.get(usertype='2', user=test)
                except ObjectDoesNotExist:
                    tourist = None

                try:
                    businessman = UserProfile.objects.get(usertype='3', user=test)
                except ObjectDoesNotExist:
                    businessman = None
                    
                if student is not None:
                    login(request, userAuth)
                    return HttpResponseRedirect('/findr/index')

                elif tourist is not None:
                    login(request, userAuth)
                    return HttpResponseRedirect('/findr/tourist')

                elif businessman is not None:
                    login(request, userAuth)
                    return HttpResponseRedirect('/findr/businessman')

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
            return HttpResponse(UserProfile.objects.all().values_list('usertype'))


    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'findr/login.htm', {})



def searchtest(request):

    if request.method == "POST":
        search_target = request.POST['search']

        result = CityInfoDetail.objects.filter(name__iexact=search_target)
        
        return render(request, "findr/resultspage.html", {'CityInfoDetails':results})
    else:
        return render(request, "findr/searchtest.html", {})






def category(request, category):
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


def itempage(request):
    return render(request, 'findr/itempage.html')