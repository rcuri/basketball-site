from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    fav_team = models.CharField(max_length=30, blank=True)

    #teams = ArrayField(models.CharField(max_length=50, blank=True), size=30)


    def __str__(self):
        return self.user.username

class Team(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.team_name



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
