import requests
from django.shortcuts import render, redirect
from .forms import PlayerSearchForm
from .models import Player

def search_player(request):
    form = PlayerSearchForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        player_name = form.cleaned_data['player_name']
        player_rating = form.cleaned_data['player_rating']

        # Replace 'YOUR_API_ENDPOINT' with the actual API endpoint URL for player search
        api_url = 'https://futdb.app/api/players/search'

        # Replace 'YOUR_AUTH_TOKEN' with your actual authentication token
        auth_token = 'aa1bc882-5c89-467e-bee1-b7d1e1be8382'

        request_body = {
            'name': player_name,
            'rating': player_rating,
        }

        try:
            response = requests.post(api_url, json=request_body, headers={'X-AUTH-TOKEN': auth_token})
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            data = response.json()

            players = data.get('items', [])
            user = request.user

            for player_data in players:
                player = Player.objects.create(
                    user=user,
                    name=player_data['name'],
                    rating=player_data['rating'],
                    position=player_data['position'],
                    nation=player_data['nation'],
                    club=player_data['club'],
                    league=player_data['league']
                )

            return render(request, 'player_search/results.html', {'players': players})

        except requests.exceptions.RequestException as e:
            return render(request, 'player_search/search.html', {'form': form, 'error_message': str(e)})

    return render(request, 'player_search/search.html', {'form': form})

def add_player(request):
    if request.method == 'POST':
        form = PlayerSearchForm(request.POST)
        if form.is_valid():
            user = request.user
            player = Player(
                user=user,
                name=form.cleaned_data['player_name'],
                rating=form.cleaned_data['player_rating'],
                # ... Fill in other player data fields ...
            )
            player.save()
            form = PlayerSearchForm()
            return render(request, 'player_search/search.html', {'form': form, 'success_message': 'Player added successfully!'})

    return redirect('player_search:search_player')

def show_players(request):
    # Get the currently logged-in user
    user = request.user

    # Retrieve players associated with the logged-in user
    players = Player.objects.filter(user=user)

    return render(request, 'player_search/show_players.html', {'players': players})

