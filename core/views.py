from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import Player, Match
from .utils import generate_fixtures 
from django.db.models import F
from django.urls import reverse
from django.contrib import messages


from django.db.models import Q, Count


# Create your views here.
from django.http import JsonResponse


#LANDING PAGE
def landing_page_view(request):
    # Score submission logic
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        home_score = request.POST.get('home_score')
        away_score = request.POST.get('away_score')

        if match_id and home_score is not None and away_score is not None:
            match = Match.objects.get(id=match_id)
            match.home_score = int(home_score)
            match.away_score = int(away_score)
            match.is_played = True
            match.save()

    # Unplayed matches
    unplayed_matches = Match.objects.filter(is_played=False).order_by('id')
    played_matches = Match.objects.filter(is_played=True).order_by('-id')

    # League table
    players = Player.objects.all()
    table = []

    for player in players:
        matches = Match.objects.filter(Q(home_player=player) | Q(away_player=player), is_played=True)
        wins = draws = losses = gf = ga = 0

        for m in matches:
            if m.home_player == player:
                gfor, gainst = m.home_score, m.away_score
            else:
                gfor, gainst = m.away_score, m.home_score

            gf += gfor
            ga += gainst

            if gfor > gainst:
                wins += 1
            elif gfor == gainst:
                draws += 1
            else:
                losses += 1

        points = wins * 3 + draws
        gd = gf - ga
        remaining = Match.objects.filter(Q(home_player=player) | Q(away_player=player), is_played=False).count()

        table.append({
            'name': player.name,
            'gp': matches.count(),
            'w': wins,
            'd': draws,
            'l': losses,
            'gf': gf,
            'ga': ga,
            'gd': gd,
            'pts': points,
            'rem': remaining
        })

    table.sort(key=lambda x: (x['pts'], x['gd'], x['gf']), reverse=True)

    return render(request, 'landing.html', {
        'matches': unplayed_matches,
        'results': played_matches,
        'table': table
    })

#PLAYOFF
def playoff_bracket_view(request):
    players = Player.objects.all()
    table = []

    for player in players:
        matches = Match.objects.filter(Q(home_player=player) | Q(away_player=player), is_played=True, is_playoff=False)
        wins = draws = losses = gf = ga = 0

        for m in matches:
            if m.home_player == player:
                gfor, gainst = m.home_score, m.away_score
            else:
                gfor, gainst = m.away_score, m.home_score

            gf += gfor
            ga += gainst

            if gfor > gainst:
                wins += 1
            elif gfor == gainst:
                draws += 1
            else:
                losses += 1

        points = wins * 3 + draws
        gd = gf - ga

        table.append({
            'player': player,
            'points': points,
            'gd': gd,
            'gf': gf
        })

    table.sort(key=lambda x: (x['points'], x['gd'], x['gf']), reverse=True)
    top4 = [entry['player'] for entry in table[:4]]

    if len(top4) < 4:
        return render(request, 'playoff.html', {'error': 'Not enough players for playoffs.'})

    # Block early playoff access if league is incomplete
    if Match.objects.filter(is_played=False, is_playoff=False).exists():
        return render(request, 'playoff.html', {
            'error': 'Playoffs will unlock after all league matches are completed. Please check back later.'
        })


    # Get or create semifinal matches
    semi1, _ = Match.objects.get_or_create(
        home_player=top4[0], away_player=top4[3],
        is_playoff=True, playoff_stage='Semi'
    )
    semi2, _ = Match.objects.get_or_create(
        home_player=top4[1], away_player=top4[2],
        is_playoff=True, playoff_stage='Semi'
    )

    # Handle playoff score submission
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        home_score = request.POST.get('home_score')
        away_score = request.POST.get('away_score')

        if match_id and home_score and away_score:
            match = Match.objects.get(id=match_id)
            match.home_score = int(home_score)
            match.away_score = int(away_score)
            match.is_played = True
            match.save()

    # Auto-generate final if both semis are played and final doesn't exist
    final_match = Match.objects.filter(is_playoff=True, playoff_stage='Final').first()

    if semi1.is_played and semi2.is_played and not final_match:
        # Determine finalists
        semi1_winner = semi1.home_player if semi1.home_score > semi1.away_score else semi1.away_player
        semi2_winner = semi2.home_player if semi2.home_score > semi2.away_score else semi2.away_player

        final_match = Match.objects.create(
            home_player=semi1_winner,
            away_player=semi2_winner,
            is_playoff=True,
            playoff_stage='Final'
        )

    return render(request, 'playoff.html', {
        'semi1': semi1,
        'semi2': semi2,
        'final_match': final_match,
        'top4': top4
    

    })


#RESET TABLE

def reset_tournament_view(request):
    if request.method == 'POST':
        # Delete all matches
        Match.objects.all().delete()

        # Re-generate fresh fixtures
        from .utils import generate_fixtures
        generate_fixtures()

        messages.success(request, "✅ Tournament reset! All matches regenerated.")
        return HttpResponseRedirect(reverse('landing'))

    return render(request, 'reset_tournament.html')



# def landing_page_view(request):
#     # Score submission logic
#     if request.method == 'POST':
#         match_id = request.POST.get('match_id')
#         home_score = request.POST.get('home_score')
#         away_score = request.POST.get('away_score')

#         if match_id and home_score is not None and away_score is not None:
#             match = Match.objects.get(id=match_id)
#             match.home_score = int(home_score)
#             match.away_score = int(away_score)
#             match.is_played = True
#             match.save()

#     # Unplayed matches
#     unplayed_matches = Match.objects.filter(is_played=False).order_by('id')
#     played_matches = Match.objects.filter(is_played=True).order_by('-id')[:10]

#     # League table
#     players = Player.objects.all()
#     table = []

#     for player in players:
#         matches = Match.objects.filter(Q(home_player=player) | Q(away_player=player), is_played=True)
#         wins = draws = losses = gf = ga = 0

#         for m in matches:
#             if m.home_player == player:
#                 gfor, gainst = m.home_score, m.away_score
#             else:
#                 gfor, gainst = m.away_score, m.home_score

#             gf += gfor
#             ga += gainst

#             if gfor > gainst:
#                 wins += 1
#             elif gfor == gainst:
#                 draws += 1
#             else:
#                 losses += 1

#         points = wins * 3 + draws
#         gd = gf - ga
#         remaining = Match.objects.filter(Q(home_player=player) | Q(away_player=player), is_played=False).count()

#         table.append({
#             'name': player.name,
#             'gp': matches.count(),
#             'w': wins,
#             'd': draws,
#             'l': losses,
#             'gf': gf,
#             'ga': ga,
#             'gd': gd,
#             'pts': points,
#             'rem': remaining
#         })

#     table.sort(key=lambda x: (x['pts'], x['gd'], x['gf']), reverse=True)

#     return render(request, 'landing.html', {
#         'matches': unplayed_matches,
#         'results': played_matches,
#         'table': table
#     })


def index(request):
    return JsonResponse({"message": "FIFA League backend is running."})


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Player.objects.create(name=name)
            return redirect('signup')  # or redirect to a success page
        
    players = Player.objects.all()    
    return render(request, 'signup.html', {'players': players})



def generate_fixture_view(request):
    message = generate_fixtures()
    return JsonResponse({"message": message})



# ✅ NEW: Score submission form for players
def player_score_submission_view(request):
    unplayed_matches = Match.objects.filter(is_played=False).order_by('id')

    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        home_score = request.POST.get('home_score')
        away_score = request.POST.get('away_score')

        if match_id and home_score is not None and away_score is not None:
            match = get_object_or_404(Match, id=match_id)
            match.home_score = int(home_score)
            match.away_score = int(away_score)
            match.is_played = True
            match.save()
            return redirect('player-submit-score')

    return render(request, 'player_score_input.html', {'matches': unplayed_matches})

# FEATURES AND RESULTS
def fixtures_results_view(request):
    upcoming = Match.objects.filter(is_played=False).order_by('id')
    completed = Match.objects.filter(is_played=True).order_by('-id')  # most recent first

    return render(request, 'fixtures_results.html', {
        'upcoming': upcoming,
        'completed': completed
    })


# LEAGUE TABLE
def league_table_view(request):
    players = Player.objects.all()
    table = []

    for player in players:
        # All matches where player was home or away
        matches = Match.objects.filter(
            Q(home_player=player) | Q(away_player=player),
            is_played=True
        )

        games_played = matches.count()
        wins = draws = losses = goals_for = goals_against = 0

        for match in matches:
            if match.home_player == player:
                gf, ga = match.home_score, match.away_score
            else:
                gf, ga = match.away_score, match.home_score

            goals_for += gf
            goals_against += ga

            if gf > ga:
                wins += 1
            elif gf == ga:
                draws += 1
            else:
                losses += 1

        points = wins * 3 + draws
        goal_diff = goals_for - goals_against
        remaining = Match.objects.filter(
            Q(home_player=player) | Q(away_player=player),
            is_played=False
        ).count()

        table.append({
            'name': player.name,
            'games_played': games_played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_diff': goal_diff,
            'points': points,
            'remaining': remaining,
        })

    # Sort by points > goal_diff > goals_for
    table.sort(key=lambda x: (x['points'], x['goal_diff'], x['goals_for']), reverse=True)

    return render(request, 'league_table.html', {'table': table})