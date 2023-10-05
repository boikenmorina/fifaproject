from django.core.management.base import BaseCommand
from player_search.models import Player
from django.db.models import Count

class Command(BaseCommand):
    help = 'Remove duplicate player entries for each user based on name and rating'

    def handle(self, *args, **kwargs):
        # Finding duplicate players for a given user based on name and rating
        duplicates = Player.objects.values('user', 'name', 'rating').annotate(name_count=Count('name')).filter(name_count__gt=1)

        for duplicate in duplicates:
            # Get IDs of all but one of the entries and delete the rest
            player_ids_to_delete = Player.objects.filter(
                user=duplicate['user'], 
                name=duplicate['name'], 
                rating=duplicate['rating']
            ).values_list('id', flat=True)[1:]
            
            Player.objects.filter(id__in=player_ids_to_delete).delete()
            
            self.stdout.write(self.style.SUCCESS(f"Removed duplicates for user {duplicate['user']} and player {duplicate['name']} with rating {duplicate['rating']}"))

        self.stdout.write(self.style.SUCCESS('Done removing duplicates!'))

