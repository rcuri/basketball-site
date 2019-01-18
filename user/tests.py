from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import date, timedelta
from django.urls import reverse
from .forms import SignUpForm
from teams.models import Team

class ProfileModelTests(TestCase):
    def test_correct_team(self):
        '''
            test whether a user's favorite team is returned correctly
        '''
        testuser = User.objects.create(username='testuser', password='password')
        testuser.profile.fav_team = 'LAL'
        self.assertEqual(testuser.profile.fav_team, 'LAL')

    def test_incorrect_team(self):
        '''
            test if you receive an error when comparing against an incorrect team
        '''
        testuser = User.objects.create(username='testuser', password='password')
        testuser.profile.fav_team = 'LAL'
        self.assertNotEqual(testuser.profile.fav_team, 'GSW')

    def test_valid_birth_date(self):
        '''
            test if a user's birth date was saved correctly
        '''
        testuser = User.objects.create(username='testuser', password='password')
        testuser.profile.birth_date = date.today()
        self.assertLessEqual(testuser.profile.birth_date, date.today())

    def test_invalid_birth_date(self):
        '''
            test if a birth date in the future is returned
        '''
        testuser = User.objects.create(username='testuser', password='password')
        testuser.profile.birth_date = date.today() + timedelta(days=1)
        self.assertGreater(testuser.profile.birth_date, date.today())


class ProfileViewTests(TestCase):
    fixtures = ['basketball/fixtures/clean_database.json']

    def test_sign_up_process(self):
        '''
            test whether all steps in the sign up process work properly. This
            includes form validation and redirecting user to another page
            after submitting sign up form.
        '''
        client = Client()
        form_data = {
            'username': 'homieman',
            'birth_date': '05/08/1995',
            'fav_team': 'LAL',
            'password1': 'password7',
            'password2': 'password7',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = client.post(reverse('signup'), form_data)
        self.assertEqual(response.status_code, 302)
        response = client.post(reverse('showteams'))
        testuser = User.objects.get(username='homieman')
        self.assertEqual(response.status_code, 200)

    def test_five_teams_assigned_signup(self):
        '''
            test whether only five teams are assigned to a user's team_set
            upon signing up for site
        '''
        client = Client()
        form_data = {
            'username': 'homieman',
            'birth_date': '05/08/1995',
            'fav_team': 'LAL',
            'password1': 'password7',
            'password2': 'password7',
        }
        form = SignUpForm(data=form_data)
        response = client.post(reverse('signup'), form_data)
        response = client.post(reverse('showteams'))
        testuser = User.objects.get(username='homieman')
        initial_team_set = testuser.profile.team_set.all()
        self.assertEqual(len(initial_team_set), 5)

    def test_home_page_logged_in(self):
        '''
            test whether a logged in user can access the home page, which
            is only accessible to logged in users
        '''
        client = Client()
        form_data = {
            'username': 'homieman',
            'birth_date': '05/08/1995',
            'fav_team': 'LAL',
            'password1': 'password7',
            'password2': 'password7',
        }
        form = SignUpForm(data=form_data)
        response = client.post(reverse('signup'), form_data)
        response = client.post(reverse('showteams'))
        testuser = User.objects.get(username='homieman')
        logged_in_response = client.get(reverse('home'))
        self.assertEqual(logged_in_response.status_code, 200)

    def test_home_page_logged_out(self):
        '''
            test whether a user is redirected upon attempting to access
            homepage, while not being signed into their account.
        '''
        client = Client()
        form_data = {
            'username': 'homieman',
            'birth_date': '05/08/1995',
            'fav_team': 'LAL',
            'password1': 'password7',
            'password2': 'password7',
        }
        form = SignUpForm(data=form_data)
        response = client.post(reverse('signup'), form_data)
        response = client.post(reverse('showteams'))
        testuser = User.objects.get(username='homieman')
        [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id')==str(testuser.id)]
        logged_out_response = client.get(reverse('home'))
        self.assertEqual(logged_out_response.status_code, 302)
