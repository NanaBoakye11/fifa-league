from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp


    def __str__(self):
        return self.name


class Match(models.Model):
    home_player = models.ForeignKey(Player, related_name='home_matches', on_delete=models.CASCADE)
    away_player = models.ForeignKey(Player, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    is_played = models.BooleanField(default=False)
    is_playoff = models.BooleanField(default=False)
    playoff_stage = models.CharField(max_length=20, blank=True, null=True)  # 'Semi', 'Final'
    match_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.home_player} vs {self.away_player}"
