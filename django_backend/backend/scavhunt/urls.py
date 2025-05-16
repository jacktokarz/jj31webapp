from django.urls  import path
from scavhunt import views

urlpatterns =  [
    path('players/', views.player_list),
    path('players/<str:id>/', views.player_detail),
    path('cards/', views.card_list),
    path('cards/<str:id>/', views.card_detail),
    path('cards/<str:id>/favorite', views.card_favorite),
    path('questions/', views.question_list),
    path('questions/<str:id>/', views.question_detail),
    path('teams/', views.team_list),
    path('teams/<str:id>/', views.team_detail)
]
