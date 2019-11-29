from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    """
    User Profile model created to extend Django's User model. Use signals
    so Profile model automatically created/updated when we create/update a
    User instances.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    fav_team = models.CharField(max_length=30, blank=True)

    def __str__(self):
        """Profile instance represented by user's username."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Hook create_user_profile to User model when save event occurs."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Hook save_user_profile to User model when save event occurs."""
    instance.profile.save()
