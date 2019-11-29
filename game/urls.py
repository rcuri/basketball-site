from django.conf.urls import url, include
from django.urls import path
from . import views


appname = 'game'
urlpatterns = [
    path('failed_test/', views.failed_test, name='failed_test'),
    path('successful_test/', views.successful_test, name='succ_test'),
    path('u/<str:username>/games/join', views.join, name='join'),
    path('u/<str:username>/games/', views.games_home, name='games_home'),
    path('games/gameid=<int:pk>/', views.game_page, name='game_page'),
    path(
        'u/<str:username>/games/pending',
        views.pending_games, name='pending_games'),
    path(
        'u/<str:username>/games/pending/delete/<int:pk>',
        views.LobbyDelete.as_view(), name='lobby_delete'),
    path(
        'u/<str:username>/games/history',
        views.history_games, name='history_games'),
    path(
        'u/<str:username>/games/active',
        views.active_games, name='active_games'),
]
