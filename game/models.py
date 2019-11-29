from django.db import models
from django.contrib.auth.models import User


class Lobby(models.Model):
    """
    Game Lobby model. Lobby deleted once new player joins and both players
    get assigned Game object.
    """
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    lineups_set = models.BooleanField(default=False)
    # TODO need to delete a lobby if it's creation date is longer than 1 day
    pub_date = models.DateTimeField(auto_now_add=True, null=True)


class Game(models.Model):
    """
    Each player involved in Game gets their own private Game instance.
    game_id is shared between two players' game to indicate that they are
    both playing against each other and only they have access to that game.
    """
    game_id = models.IntegerField(default=0)
    game_date = models.DateField(auto_now_add=True, null=True)
    own_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    opponent_name = models.CharField(max_length=30, null=True)
    is_complete = models.BooleanField(default=False)
    lineups_set = models.BooleanField(default=False)

    def __str__(self):
        """Game object is represented by the game's primary key."""
        return str(self.id)
