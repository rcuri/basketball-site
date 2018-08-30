from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views


appname = 'homepage'
urlpatterns = [
    path('', views.index, name='index'),
    path('user/', views.userhome, name='userhome'),
    path('', include('user.urls')),
    path('', include('game.urls')),
]
