from django.conf.urls import url

from . import views

urlpatterns = [
	# this set up the url as ....../index, and view.index
	# open up views.py function call index.
    url(r'^student/', views.index, name='index'),
    url(r'^tourist/', views.tourist, name='tourist'),
    url(r'^businessman/', views.businessman, name='businessman'),
    url(r'^admin/', views.admin, name='admin'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^welcome/', views.welcome, name='welcome'),
    url(r'^itempage/', views.itempage, name='welcome'),
    url(r'(?P<category>.*)/$', views.category),
 

    url(r'^searchtest/', views.searchtest, name='welcome')
]
