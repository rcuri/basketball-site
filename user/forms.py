from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    """
    SignUpForm extends UserCreationForm by adding birth date (birth_date) and
    favorite team (fav_team) attributes.
    """
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
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
        ('PHO', 'Phoenix Suns'),
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
    fav_team = forms.ChoiceField(
        choices=NBA_TEAMS,
        help_text='''Your favorite team will have a higher chance of being
        selected as one of your 5 teams.''')

    class Meta:
        """Meta class provides metadata to SignUpForm."""
        model = User
        fields = ('username', 'birth_date', 'fav_team',
                  'password1', 'password2')
