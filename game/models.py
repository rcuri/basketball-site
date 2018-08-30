from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lobby(models.Model):
    # Might need to make this to bigIntegerField as I scale up
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    lineups_set = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)


    # Need to delete a lobby if it's creation date is longer than 1 day
    # date_created = models.DateField()




class Game(models.Model):
    own_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    opponent_name = models.CharField(max_length=30, null=True)
    is_complete = models.BooleanField(default=False)
    lineups_set = models.BooleanField(default=False)
    game_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)
