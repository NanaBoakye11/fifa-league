from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing'),
    path('generate-fixtures/', views.generate_fixture_view, name='generate-fixtures'),
    path('submit-score/', views.player_score_submission_view, name='player-submit-score'),
    path('generate-fixtures/', views.generate_fixture_view, name='generate-fixtures'),
    path('league-table/', views.league_table_view, name='league-table'),
    path('fixtures-results/', views.fixtures_results_view, name='fixtures-results'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.landing_page_view, name='landing'),
    path('playoffs/', views.playoff_bracket_view, name='playoffs'),
    path('reset-tournament/', views.reset_tournament_view, name='reset-tournament'),


]
