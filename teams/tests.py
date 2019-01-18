from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from datetime import date
from .models import Team, Player

class TeamModelTests(TestCase):
    fixtures = ['basketball/fixtures/clean_database.json']

    def test_valid_team_abbreviation_length(self):
        '''
            test whether each team_name variable has length of 3
        '''
        for team in Team.objects.all():
            self.assertEqual(len(team.team_name),3)

    def test_valid_team_name(self):
        '''
            test whether each team_name belongs to a current nba team
        '''
        team_list = [
            'ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN',
            'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
            'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX',
            'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
        ]
        for team in Team.objects.all():
            self.assertIn(team.team_name, team_list)

    def test_valid_season(self):
        '''
            test whether team's season is a previous or current season. If
            team's season's year is in the future, raise error.
        '''
        current_yr = int(date.today().year)
        for team in Team.objects.all():
            self.assertLessEqual(team.season, current_yr)

    def test_valid_total_teams(self):
        '''
            test whether the total number of teams for a season is the same
            as the total number of teams in our database. Change value of
            total_num_teams if NBA expands the league.
        '''
        total_num_teams = 30
        self.assertEqual(Team.objects.all().count(), total_num_teams)

    @classmethod
    def tearDownClass(self):
        super(TeamModelTests, self).tearDownClass()



class PlayerModelTests(TestCase):
    fixtures = ['basketball/fixtures/clean_database.json']

    def test_valid_team(self):
        '''
            test whether each player's assigned team exists in the team
            data set
        '''
        teams = Team.objects.all()
        try:
            for player in Player.objects.all():
                player.team in teams
        except ObjectDoesNotExist:
            self.fail("This team does not exist in the database")


    def test_player_name_not_blank(self):
        '''
            test to ensure player's name is not left blank
        '''
        for player in Player.objects.all():
            self.assertGreater(len(player.player_name), 0)
            self.assertNotEqual(player.player_name, ' ')

    def test_player_valid_position(self):
        '''
            test whether the player's season is not set in the future
        '''
        valid_positions = ['PG', 'SG', 'SF', 'PF', 'C']
        for player in Player.objects.all():
            self.assertIn(player.position, valid_positions)

    def test_valid_height(self):
        '''
            test whether the player's height is valid
        '''
        for player in Player.objects.all():
            self.assertGreater(player.height, '0')

    def test_valid_weight(self):
        '''
            test whether the player's weight is valid. 100lbs is minimum wt in
            order to have a reasonable lower limit.
        '''
        for player in Player.objects.all():
            self.assertGreater(player.weight, 100)

    def test_valid_birth_date_future(self):
        '''
            test whether birth date is not set in the future
        '''
        future_yr = date.today().year + 1
        for player in Player.objects.all():
            yr_born = int(player.birth_date[-4:])
            self.assertLess(yr_born, future_yr)

    def test_elegible_age_nba(self):
        '''
            test whether the player's listed age meets the 19 year old minimum
            age requirement to sign with an NBA team
        '''
        current_yr = date.today().year
        for player in Player.objects.all():
            yr_born = int(player.birth_date[-4:])
            age = current_yr - yr_born
            self.assertGreaterEqual(age, 19)

    @classmethod
    def tearDownClass(self):
        super(PlayerModelTests, self).tearDownClass()

class TeamsViewTest(TestCase):
    fixtures = ['basketball/fixtures/profiles_loaded.json']

    def test_teams_page_accessible_logged_in(self):
        '''
            test to see if user is shown their teams page if they try to
            access it while logged into their account
        '''
        client = Client()
        user = User.objects.get(username='rodrigocuriel')
        self.client.force_login(user)
        response = self.client.get(reverse('displayteams', kwargs= {'username':'rodrigocuriel'}))
        self.assertEqual(response.status_code, 200)

    def test_teams_page_inaccessible_logged_out(self):
        '''
            test to see if user is redirected to the 'index' page if they try
            to access another user's teams page
        '''
        client = Client()
        response = self.client.get(reverse('displayteams', kwargs={'username':'rodrigocuriel'}))
        self.assertEqual(response.status_code, 302)

    @classmethod
    def tearDownClass(self):
        super(TeamsViewTest, self).tearDownClass()
