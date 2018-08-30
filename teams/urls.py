from django.urls import path
from django.conf.urls import url, include

from . import views

appname = 'teams'
urlpatterns = [
    path('u/<str:username>/teams', views.displayteams, name='displayteams'),
    path('', include('game.urls')),
]
