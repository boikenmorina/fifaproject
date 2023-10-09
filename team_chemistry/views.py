from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from player_search.models import Player
import json
from collections import Counter
from player_search.serializers import PlayerSerializer

@csrf_exempt
def calculate_team_chemistry(request):
    if request.method == 'POST':
        try:
            # Parse the received data
            selected_players_data = json.loads(request.body)['selected_players']
            all_players = [Player.objects.get(id=data['player_id']) for data in selected_players_data]

            # Clean positions and gather valid players
            valid_players = []
            for data in selected_players_data:
                data['selected_position'] = ''.join([i for i in data['selected_position'] if not i.isdigit()])
                player = Player.objects.get(id=data['player_id'])
                if player.position == data['selected_position']:
                    player.chemistry = 0  # Resetting chemistry
                    valid_players.append(player)

            # League Chemistry
            unique_leagues = set(player.club.league for player in valid_players if player.club is not None)

            for league in unique_leagues:
                league_players = [player for player in valid_players if player.club is not None and player.club.league == league]
                league_count = len(league_players)

                if 3 <= league_count <= 4:
                    increment = 1
                elif 5 <= league_count <= 7:
                    increment = 2
                elif 8 <= league_count <= 11:
                    increment = 3
                else:
                    increment = 0

                for player in league_players:
                    player.chemistry += increment

            # Club Chemistry
            unique_clubs = set(player.club for player in valid_players)
            for club in unique_clubs:
                club_players = [player for player in valid_players if player.club == club]
                club_count = len(club_players)

                if 2 <= club_count <= 3:
                    increment = 1
                elif 4 <= club_count <= 6:
                    increment = 2
                elif 7 <= club_count <= 11:
                    increment = 3
                else:
                    increment = 0

                for player in club_players:
                    player.chemistry += increment

            # Country Chemistry
            unique_nations = set(player.nation for player in valid_players)
            for nation in unique_nations:
                nation_players = [player for player in valid_players if player.nation == nation]
                nation_count = len(nation_players)

                if 2 <= nation_count <= 4:
                    increment = 1
                elif 5 <= nation_count <= 7:
                    increment = 2
                elif 8 <= nation_count <= 11:
                    increment = 3
                else:
                    increment = 0

                for player in nation_players:
                    player.chemistry += increment

            # Cap chemistry and compute total chemistry
            total_chemistry = sum(min(player.chemistry, 3) for player in valid_players)
            total_rating = sum(player.rating for player in all_players)
            average_rating = round(total_rating / 11)

            response_data = {
                'total_chemistry': total_chemistry,
                'average_rating': average_rating
                
                }

            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def suggest_players(request):
    try:
        # Parse the received data
        selected_players_data = json.loads(request.body)['selected_players']
        all_players = [Player.objects.get(id=data['player_id']) for data in selected_players_data]
        selected_player_ids = [player.id for player in all_players]

        # Detect empty positions
        all_positions = ['GK', 'CB', 'CB', 'CM', 'CM', 'LB', 'RB', 'ST', 'ST', 'LM', 'RM']
        filled_positions_raw = {data['selected_position'] for data in selected_players_data}
        from collections import defaultdict
        filled_positions_count = defaultdict(int)
        for position in filled_positions_raw:
            sanitized_position = ''.join([i for i in position if not i.isdigit()])
            filled_positions_count[sanitized_position] += 1

        empty_positions = []

# Determine which positions are still empty
        for pos in all_positions:
            if filled_positions_count[pos] > 0:
               filled_positions_count[pos] -= 1
            else:
                empty_positions.append(pos)                 

        # Find most common league and nation
        leagues = [player.club.league for player in all_players if player.club]
        nations = [player.nation for player in all_players if player.nation]
        most_common_league = Counter(leagues).most_common(1)[0][0]
        most_common_nation = Counter(nations).most_common(1)[0][0]

        # Suggest players based on empty positions and most common league/nation
        league_suggestions = Player.objects.filter(position__in=empty_positions, club__league=most_common_league).exclude(id__in=selected_player_ids)[:2]
        nation_suggestions = Player.objects.filter(position__in=empty_positions, nation=most_common_nation).exclude(id__in=selected_player_ids)[:2]

        serialized_league_suggestions = [PlayerSerializer(player).data for player in league_suggestions]
        serialized_nation_suggestions = [PlayerSerializer(player).data for player in nation_suggestions]

        suggestions = {
            'league_suggestions': serialized_league_suggestions,
            'nation_suggestions': serialized_nation_suggestions
        }

        return JsonResponse(suggestions, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)