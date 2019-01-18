from django.db import models
from user.models import Profile

class Team(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)
    team_name = models.CharField(max_length=30, blank=True)
    season = models.IntegerField(default=1900)

    def __str__(self):
        return self.team_name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=5, blank=True)
    height = models.CharField(max_length=5, blank=True)
    weight = models.IntegerField(default=150)
    birth_date = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.player_name
