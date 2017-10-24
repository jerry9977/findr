from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    url(r'^index/', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^welcome/', views.welcome, name='welcome'),
    url(r'^itempage/', views.itempage, name='itempage'),
    url(r'^search/', views.search, name='search'),
    
    url(r'(?P<category>.*)/$', views.category),
 

   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
