from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from .models import Lobby, Game


def failed_test(request):
    """Temporary page for illegal access."""
    return HttpResponse("You do not have access to this page.")


def successful_test(request):
    """Temporary page for successful access."""
    # TODO Might be ready to remove
    return HttpResponse("Success!")


@login_required
def join(request, username):
    """
    Join a lobby if available, else create a lobby and wait for it to
    be joined.
    """
    # Ensures people aren't signing up for a lobby they created
    available_lobbies =  Lobby.objects.exclude(
                            created_by=request.user).order_by('pub_date')
    if available_lobbies.count() == 0:
        Lobby(created_by=request.user).save()
        return redirect('pending_games', username)
    else:
        # TODO Need lock on database to ensure two players don't sign up for
        # the same lobby
        cur_lobby = available_lobbies.first()
        host_user = cur_lobby.created_by

        game_host = Game(
            own_user=host_user,
            opponent_name=request.user.username)
        game_opp = Game(
            own_user=request.user,
            opponent_name=host_user.username)
        game_host.save()
        game_opp.save()

        # Need to commit game object in order to link by primary key (id)
        game_host.game_id = game_host.id
        game_opp.game_id = game_host.id
        game_host.save()
        game_opp.save()
        cur_lobby.delete()
        return redirect('game_page', pk=game_host.game_id )


@login_required
def games_home(request, username):
    """
    Show all available games of logged in user. Redirect if attempting to
    view other user's games.
    """
    if request.user.username != username:
    # TODO Replace this temp page
        return redirect('failed_test')
    else:
        return render(request, 'game/game_home.html')


@login_required
def pending_games(request, username):
    """
    Show all pending lobbies of logged in user. Redirect if attempting to
    view other user's lobbies.
    """
    if request.user.username != username:
    # TODO Replace this temp page
        return redirect('failed_test')
    else:
        pending = request.user.lobby_set.order_by('-pub_date').filter(
            pub_date__date = timezone.now())
        return render(
            request, 'game/pending_games.html', {'pending': pending})


class LobbyDelete(DeleteView):
    model = Lobby
    def get_success_url(self):
        username = self.object.created_by.username
        return reverse('pending_games', args=[username])


# TODO change this so we replace lobby with actual finished games
def history_games(request, username):
    """
    Show all completed games of logged in user. Redirect if attempting to
    view other user's game history.
    """
    if request.user.username != username:
    # TODO Fix this
        return redirect('failed_test')
    else:
        finished = request.user.lobby_set.order_by('-pub_date').filter(
            pub_date__date = timezone.now())
        return render(
            request, 'game/history_games.html', {'finished': finished})


def active_games(request, username):
    """
    Show all active games of logged in user. Redirect if attempting to
    view other user's active games.
    """
    if request.user.username != username:
    # TODO Fix this
        return redirect('failed_test')
    else:
        active = request.user.game_set.filter(is_complete=False)
        return render(request, 'game/active_games.html', {'active': active})


def game_page(request, pk):
    """
    Show current game page if game's linked primary key (pk) is present in
    user's active games. Redirect if not present.
    """
    owns_game = request.user.game_set.filter(game_id=pk)
    if owns_game.count() == 0:
        return redirect('failed_test')
    else:
        game = request.user.game_set.get(game_id=pk)
        teams = request.user.profile.team_set.all()
        return render(
            request, 'game/game_page.html', {'game': game, 'teams': teams})
