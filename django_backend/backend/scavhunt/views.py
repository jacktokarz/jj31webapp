from django.http import JsonResponse, Http404, HttpResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
import scavhunt.serializer as sl
import scavhunt.discordsender as ds
from scavhunt.fetcherprovider import FetcherProvider

# Create your views here.

fetcher = FetcherProvider(True).get_fetcher()

def player_list(request):

    if request.method == 'GET':
        serializer = sl.PlayerSerializer(fetcher.get_all_players(), many = True)
        return JsonResponse(serializer.data, safe=False)

def player_detail(request, id):
    player = fetcher.get_player(id)

    if player == None:
        raise Http404

    if request.method == 'GET':
        serializer = sl.PlayerSerializer(player)
        return JsonResponse(serializer.data)

def card_list(request):
    if request.method == 'GET':
        serializer = sl.CardSerializer(fetcher.get_all_cards(), many = True)
        return JsonResponse(serializer.data, safe=False)

def card_detail(request, id):
    card = fetcher.get_card(id)

    if card == None:
        raise Http404 

    if request.method == 'GET':
        serializered = sl.CardSerializer(card)
        return JsonResponse(serializered.data)
    
def question_list(request):

    if request.method == 'GET':
        serializer = sl.QuestionSerializer(fetcher.get_all_questions(), many = True)
        return JsonResponse(serializer.data, safe=False)
    
@api_view(['GET', 'POST'])
def question_detail(request, id):
    question = fetcher.get_question(id)

    if question == None:
        raise Http404

    if request.method == 'GET':
        serialized = sl.QuestionSerializer(question)
        return JsonResponse(serialized.data)
    
    if request.method == 'POST':
        sender = ds.DiscordSender()
        sender.post_question(question, request.data["team_id"], "")
        return HttpResponse("Success")

@api_view(['POST'])
def card_favorite(request, id):
    card = fetcher.get_card(id)

    if card == None:
        raise Http404
    
    if request.method == 'POST':
        if (request.data["team_id"] is None):
            raise HttpResponseBadRequest
        fetcher.favorite_question(request.data["team_id"], id)
        return HttpResponse("Success")
    
def card_unfavorite(request, id):
    card = fetcher.get_card(id)

    if card == None:
        raise Http404
    
    if request.method == 'POST':
        if (request.data["team_id"] is None):
            raise HttpResponseBadRequest
        fetcher.favorite_question(request.data["team_id"], id)
        return HttpResponse("Success")


def team_list(request):

    if request.method == 'GET':
        serializer = sl.TeamSerializer(fetcher.get_all_teams(), many = True)
        return JsonResponse(serializer.data, safe=False)

def team_detail(request, id):
    team = fetcher.get_team(id)

    if team == None:
        raise Http404

    if request.method == 'GET':
        serialized =  sl.TeamSerializer(team)
        return JsonResponse(serialized.data)
