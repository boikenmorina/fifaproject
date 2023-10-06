import requests
from django.shortcuts import render, redirect
from .forms import PlayerSearchForm
from .models import Player, Nation, Club, League
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


import requests

def add_player(request, player_id):
    # Extract player data from request or session
    players = request.session.get('search_results')
    selected_player = next((p for p in players if p['id'] == player_id), None)

    if not selected_player:
        messages.error(request, "Couldn't find the selected player.")
        return redirect('player_search:search_player')

    # API Base and Headers
    api_base = 'https://futdb.app/api/'
    headers = {'X-AUTH-TOKEN': 'aa1bc882-5c89-467e-bee1-b7d1e1be8382'}

    # Fetch Nation, Club, and League information
    try:
        nation_response = requests.get(f"{api_base}nations/{selected_player['nation']}", headers=headers)
        nation_response.raise_for_status()
        nation_data = nation_response.json()
        print(f"Nation Data: {nation_data}") 

        club_response = requests.get(f"{api_base}clubs/{selected_player['club']}", headers=headers)
        club_response.raise_for_status()
        club_data = club_response.json()

        league_response = requests.get(f"{api_base}leagues/{selected_player['league']}", headers=headers)
        league_response.raise_for_status()
        league_data = league_response.json()

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching additional player data: {e}")
        return redirect('player_search:search_player')

    # Store to database
    nation_obj, _ = Nation.objects.get_or_create(nation_id=nation_data['nation']['id'], defaults={'name': nation_data['nation']['name']})
    league_obj, _ = League.objects.get_or_create(league_id=league_data['league']['id'], defaults={'name': league_data['league']['name']})
    club_obj, _ = Club.objects.get_or_create(club_id=club_data['club']['id'], defaults={'name': club_data['club']['name'], 'league': league_obj})

    Player.objects.create(
        user=request.user,
        name=selected_player['name'],
        rating=selected_player['rating'],
        position=selected_player['position'],
        nation=nation_obj,
        club=club_obj
        
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
        return JsonResponse({"error": "User not authenticated"})

    user = request.user.id
    players = Player.objects.filter(user=user).order_by('-rating')

    data = {
        "leagues": defaultdict(lambda: {
            "clubs": defaultdict(list)
        }),
        "nations": defaultdict(list),
    }

    for player in players:
        data["leagues"][player.club.league.name]["clubs"][player.club.name].append(PlayerSerializer(player).data)
        data["nations"][player.nation.name].append(PlayerSerializer(player).data)

    return JsonResponse(data)

