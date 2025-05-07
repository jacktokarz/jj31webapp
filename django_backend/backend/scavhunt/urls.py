from django.urls  import path
from scavhunt import views

urlpatterns =  [
    path('player/<str:id>/', views.player_detail),
    path('card/<str:id>/', views.card_detail),
    path('question/<str:id>/', views.question_detail),
    path('team/<str:id>/', views.team_detail)
]
