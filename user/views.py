from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from teams.models import Team
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.http import HttpResponse

from random import *

@login_required
def home(request):
    """Render home page for logged-in user if user is authenticated."""
    return render(request, 'user/home.html')

def signup(request):
    """
    Render signup form if invalid form is submitted or if GET request is
    sent. Create user profile and redirect to user's starting team set if
    form is valid.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Load profile instance created by create_user_profile signal
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.fav_team = form.cleaned_data.get('fav_team')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('showteams')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

@login_required
def startingteams(request):
    """Randomly assign 5 teams to user's profile upon user signup."""
    current_user = request.user
    NBA_TEAMS = (
        ('POR', 'Portland Trailblazers'),
        ('SAC', 'Sacramento Kings'),
        ('TOR', 'Toronto Raptors'),
        ('HOU', 'Houston Rockets'),
        ('LAL', 'Los Angeles Lakers'),
        ('TOR', 'Toronto Raptors'),
        ('DEN', 'Denver Nuggets'),
        ('NOP', 'New Orleans Pelicans'),
        ('UTA', 'Utah Jazz'),
        ('GSW', 'Golden State Warriors'),
        ('MEM', 'Memphis Grizzlies'),
        ('PHI', 'Philadelphia 76ers'),
        ('SAS', 'San Antonio Spurs'),
        ('PHX', 'Phoenix Suns'),
        ('OKC', 'Oklahoma City Thunder'),
        ('LAC', 'Los Angeles Clippers'),
        ('MIL', 'Milwaukee Bucks'),
        ('MIN', 'Minnesota Timberwolves'),
        ('ORL', 'Orlando Magic'),
        ('MIA', 'Miami Heat'),
        ('CLE', 'Cleveland Cavaliers'),
        ('CHA', 'Charlotte Hornets'),
        ('DET', 'Detroit Pistons'),
        ('BKN', 'Brooklyn Nets'),
        ('NYK', 'New York Knicks'),
        ('IND', 'Indiana Pacers'),
        ('ATL', 'Atlanta Hawks'),
        ('CHI', 'Chicago Bulls'),
        ('BOS', 'Boston Celtics'),
        ('DAL', 'Dallas Mavericks'),
    )
    team_list = [x for x,_ in NBA_TEAMS]

    while current_user.profile.team_set.all().count() < 5:
        rand_int = randint(0,29)
        if current_user.profile.team_set.all().filter(
                team_name=team_list[rand_int]).exists() is False:
            name = team_list[rand_int]
            team = Team.objects.get(team_name=name)
            current_user.profile.team_set.add(team)

    teams = current_user.profile.team_set.all()[:5]

    return render(request, 'user/showteams.html', {'teams': teams})
