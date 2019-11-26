"""
basketball url pattern configuration list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('homepage.urls')),
    path('', include('teams.urls')),
    path('', include('user.urls')),
    path('', include('game.urls')),
    path('admin/', admin.site.urls),
]
