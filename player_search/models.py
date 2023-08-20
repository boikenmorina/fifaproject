from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null =True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    position = models.CharField(max_length=50)
    nation = models.CharField(max_length=50)
    club = models.CharField(max_length=100)
    league = models.CharField(max_length=100)

    def __str__(self):
        return self.name

