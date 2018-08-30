from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from .models import Lobby, Game

def failed_test(request):
    return HttpResponse("You do not have access to this page.")

def successful_test(request):
    return HttpResponse("Success!")

@login_required
def join(request, username):
    # ensures people aren't signing up for a lobby they created
    available_lobbies =  Lobby.objects.exclude(created_by=request.user).order_by('pub_date')
    if available_lobbies.count() == 0:
        Lobby(created_by=request.user).save()
        return redirect('pending_games', username)
    else:
        # TODO Need something to ensure two players don't sign up for the same lobby
        cur_lobby = available_lobbies.first()
        host_user = cur_lobby.created_by

        game_host = Game(own_user=host_user, opponent_name=request.user.username)
        game_opp = Game(own_user=request.user, opponent_name=host_user.username)
        game_host.save()
        game_opp.save()

        game_host.game_id = game_host.id
        game_opp.game_id = game_host.id
        game_host.save()
        game_opp.save()
        cur_lobby.delete()
        # redirect to something like games/active_games/gameid= <gameid>
        return redirect('game_page', pk=game_host.game_id )

@login_required
def games_home(request, username):
    if request.user.username != username:
    # TODO fix this temp code
        return redirect('failed_test')
    else:
        return render(request, 'game/game_home.html')

@login_required
def pending_games(request, username):
    if request.user.username != username:
    # TODO Fix this
        return redirect('failed_test')
    else:
        # TODO might need to swap order_by & filter
        pending = request.user.lobby_set.order_by('-pub_date').filter(pub_date__date = timezone.now())
        return render(request, 'game/pending_games.html', {'pending': pending})

class LobbyDelete(DeleteView):
    model = Lobby
    def get_success_url(self):
        username = self.object.created_by.username
        return reverse('pending_games', args=[username])

# TODO change this so we replace lobby with actual games
def history_games(request, username):
    if request.user.username != username:
    # TODO Fix this
        return redirect('failed_test')
    else:
        # TODO might need to swap order_by & filter
        pending = request.user.lobby_set.order_by('-pub_date').filter(pub_date__date = timezone.now())
        return render(request, 'game/history_games.html', {'pending': pending})

def active_games(request, username):
    if request.user.username != username:
    # TODO fix this
        return redirect('failed_test')
    else:
        active = request.user.game_set.filter(is_complete=False)
        return render(request, 'game/active_games.html', {'active': active})

def game_page(request, pk):
    owns_game = request.user.game_set.filter(game_id=pk)
    if owns_game.count() == 0:
        return redirect('failed_test')
    else:
        game = request.user.game_set.get(game_id=pk)
        return render(request, 'game/game_page.html', {'game': game})
