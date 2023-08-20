from django.urls import path
from . import views

app_name = 'player_search'

urlpatterns = [
    path('', views.search_player, name='search_player'),
    path('add_player/', views.add_player, name='add_player'),
     path('show_players/', views.show_players, name='show_players'),
]
