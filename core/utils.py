from itertools import combinations
from .models import Player, Match

def generate_fixtures():
    players = list(Player.objects.all())
    if len(players) < 2:
        return "Not enough players to generate fixtures."

    matches_created = 0
    for p1, p2 in combinations(players, 2):
        # Create home and away matches
        Match.objects.create(home_player=p1, away_player=p2)
        Match.objects.create(home_player=p2, away_player=p1)
        matches_created += 2

    return f"{matches_created} matches generated."
