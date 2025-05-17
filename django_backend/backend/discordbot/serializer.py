from rest_framework import serializers

class PlayerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

class CardSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    value = serializers.IntegerField()
    team_ids = serializers.ListField()
    difficulty = serializers.CharField()

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()

class QuestionSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    cost = serializers.IntegerField()
    category = serializers.CharField()
    additional_info = serializers.CharField()
    
class TeamSerializer(serializers.Serializer):
    id = serializers.CharField()
    players = PlayerSerializer(many=True)
    name = serializers.CharField()
    points = serializers.IntegerField()
    discord_id = serializers.IntegerField()
    completed_cards = CardSerializer(many=True)
    favorite_cards = CardSerializer(many=True)
    asked_questions = QuestionSerializer(many=True)
    key = serializers.CharField()