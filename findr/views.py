from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse





def index(request):

    return render(request, 'findr/index.html')

# def index(request):
#     retdict = {'articles': Article.objects.all(),}
#     return render_to_response('findr/index.html', retdict, context_instance=RequestContext(request))


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

