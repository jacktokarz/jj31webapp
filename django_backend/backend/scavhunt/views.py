from django.http import JsonResponse
import scavhunt.local_schema as schem
from scavhunt.serializer import PlayerSerializer

# Create your views here.

def player_detail(request, id):
    player = schem.Player(id, "Foreign Punch")

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return JsonResponse(serializer.data)
