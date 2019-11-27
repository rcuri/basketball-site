from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views as core_views

appname = 'user'
urlpatterns = [
    path('user/home', core_views.home, name='home'),
    path(
        'user/login', auth_views.login,
        {'template_name': 'user/login.html'}, name='login'),
    path('user/logout', auth_views.logout,
        {'next_page': 'login'}, name='logout'),
    path('user/signup', core_views.signup, name='signup'),
    path('user/showteams', core_views.startingteams, name='showteams'),
]
