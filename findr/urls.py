from django.conf.urls import url

from . import views

urlpatterns = [
	# this set up the url as ....../index, and view.index
	# open up views.py function call index.
    url(r'^index/', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^welcome/', views.welcome, name='welcome'),

    url(r'(?P<category>.*)/$', views.category),
 

    url(r'^searchtest/', views.searchtest, name='welcome')
]
