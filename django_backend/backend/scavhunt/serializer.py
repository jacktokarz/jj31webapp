from rest_framework import serializers
import scavhunt.local_schema as schem

class PlayerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
