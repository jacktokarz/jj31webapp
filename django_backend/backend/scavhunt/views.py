from django.http import JsonResponse
import scavhunt.local_schema as schem
import scavhunt.serializer as sl

# Create your views here.

def player_detail(request, id):
    player = schem.Player(id, "Foreign Punch")

    if request.method == 'GET':
        serializer = sl.PlayerSerializer(player)
        return JsonResponse(serializer.data)

def card_detail(request, id):
    card = schem.Card(id, "Title",  "Description of a card", 400)

    if request.method == 'GET':
        serializered = sl.CardSerializer(card)
        return JsonResponse(serializered.data)

def question_detail(request, id):
    question = schem.Question("A question", "A  descripiton", 20, "Category",  True)

    if request.method == 'GET':
        serialized = sl.QuestionSerializer(question)
        return JsonResponse(serialized.data)

def team_detail(request, id):
    team = schem.Team(
        "ID",
        [schem.Player("pID", "JJ"), schem.Player("pID2", "Jack")],
        "Foreign Punch",
        30,
        [schem.Card("cID", "Card", "Description", 20),
             schem.Card("cId2", "Jump off a bridge, lmao", "Do it I dare", 1000)],
        [schem.Card("cID", "Card", "Description", 20),
             schem.Card("cId2", "Jump off a bridge, lmao", "Do it I dare", 1000)],
        [schem.Question("Title", "Desc", 100, "Cat", True)]
    )

    if request.method == 'GET':
        serialized =  sl.TeamSerializer(team)
        return JsonResponse(serialized.data)
