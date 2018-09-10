from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=30, blank=True)
    season = models.IntegerField(default=1900)

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=200, blank=True)
    position = models.CharField(max_length=5, blank=True)
    height = models.CharField(max_length=5, blank=True)
    weight = models.IntegerField(default=150)
    birth_date = models.CharField(max_length=30, blank=True)
