from django.urls import path
from . import views

app_name = 'player_search'

urlpatterns = [
    path('', views.search_player, name='search_player'),
]
