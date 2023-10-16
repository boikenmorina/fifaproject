# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calculate_chemistry/', views.calculate_team_chemistry, name='calculate_team_chemistry'),
    path('suggest_players/', views.suggest_players, name='suggest_players'),
    path('team_submit/', views.team_submit, name='team_submit'),
    path('display_teams/', views.display_teams, name='display_teams'),
    # ... your other URL patterns
]
