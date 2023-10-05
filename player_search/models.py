from django.db import models
from django.contrib.auth.models import User

class League(models.Model):
    league_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Nation(models.Model):
    nation_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Club(models.Model):
    club_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    position = models.CharField(max_length=50)
    nation = models.ForeignKey(Nation, on_delete=models.SET_NULL, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

