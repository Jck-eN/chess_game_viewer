from django.db import models


# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=1, null=True)
    time = models.DecimalField(max_digits=5, decimal_places=1, default=0, null=True)
    time_add = models.DecimalField(max_digits=5, decimal_places=1, default=0, null=True)
    date = models.DateField(null=True)


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    club = models.CharField(max_length=50, null=True)


class Game(models.Model):
    white_player_id = models.ForeignKey(Player, related_name='white',  on_delete=models.CASCADE)
    black_player_id = models.ForeignKey(Player, related_name='black', on_delete=models.CASCADE)
    result = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    pgn = models.TextField(max_length=5000)
