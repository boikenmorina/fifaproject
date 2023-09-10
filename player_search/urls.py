from django.urls import path
from . import views

app_name = 'player_search'

urlpatterns = [
    
    path('', views.search_player, name='search_player'),
    path('add_player/<int:player_id>/', views.add_player, name='add_player'),  # Notice the addition of the player_id argument
    path('show_players/', views.show_players, name='show_players'),
    path('api/players/data/', views.get_all_data, name='get-all-data'),

   

]
