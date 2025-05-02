from django.urls  import path
from scavhunt import views

urlpatterns =  [
    path('player/<str:id>/', views.player_detail)
]