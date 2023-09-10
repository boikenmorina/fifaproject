import requests
from django.shortcuts import render, redirect
from .forms import PlayerSearchForm
from .models import Player
from django.contrib import messages
from .serializers import PlayerSerializer
from django.http import JsonResponse
from collections import defaultdict
from django.contrib.auth.decorators import login_required




def search_player(request):
    form = PlayerSearchForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        player_name = form.cleaned_data['player_name']
        player_rating = form.cleaned_data['player_rating']

        api_url = 'https://futdb.app/api/players/search'
        auth_token = 'aa1bc882-5c89-467e-bee1-b7d1e1be8382'
        request_body = {'name': player_name, 'rating': player_rating}

        try:
            response = requests.post(api_url, json=request_body, headers={'X-AUTH-TOKEN': auth_token})
            response.raise_for_status()  
            data = response.json()

            players = data.get('items', [])

            # Store the players in the session for later access
            request.session['search_results'] = players

            return render(request, 'player_search/results.html', {'players': players, 'form': form})

        except requests.exceptions.RequestException as e:
            return render(request, 'player_search/search.html', {'form': form, 'error_message': str(e)})

    return render(request, 'player_search/search.html', {'form': form})


def add_player(request, player_id):
    # Extract player data from request or session (whichever method you've chosen)
    players = request.session.get('search_results')
    selected_player = next((p for p in players if p['id'] == player_id), None)

    if not selected_player:
        messages.error(request, "Couldn't find the selected player.")
        return redirect('player_search:search_player')

    # Extract player data and save to the database
    Player.objects.create(
        user=request.user,
        name=selected_player['name'],
        rating=selected_player['rating'],
        position=selected_player['position'],
        nation=selected_player['nation'],
        club=selected_player['club'],
        league=selected_player['league']
    )

    messages.success(request, 'Player added successfully!')
    return redirect('player_search:search_player')

def show_players(request):
    # Get the currently logged-in user
    user = request.user

    # Retrieve players associated with the logged-in user
    players = Player.objects.filter(user=user)

    return render(request, 'player_search/show_players.html', {'players': players})




def get_all_data(request):
    if not request.user.is_authenticated:
        # Return a default response or an error for unauthenticated users
        return JsonResponse({"error": "User not authenticated"})
    user = request.user.id
    players = Player.objects.filter(user=user).order_by('-rating')

    # Organize players by league, club, and country
    data = {
        "leagues": defaultdict(list),
        "clubs": defaultdict(list),
        "nations": defaultdict(list),
    }

    for player in players:
        data["leagues"][player.league].append(PlayerSerializer(player).data)
        data["clubs"][player.club].append(PlayerSerializer(player).data)
        data["nations"][player.nation].append(PlayerSerializer(player).data)

    return JsonResponse(data)
