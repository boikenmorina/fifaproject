# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calculate_chemistry/', views.calculate_team_chemistry, name='calculate_team_chemistry'),
    # ... your other URL patterns
]
