from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    
    name = models.CharField(max_length=100)
    submission_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    chemistry = models.IntegerField()
    player_names = models.TextField()  # This will store the player names as a comma-separated string

    def __str__(self):
        return self.name

