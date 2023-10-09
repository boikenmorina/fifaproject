# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calculate_chemistry/', views.calculate_team_chemistry, name='calculate_team_chemistry'),
    path('suggest_players/', views.suggest_players, name='suggest_players'),
    # ... your other URL patterns
]
