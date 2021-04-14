from rest_framework import serializers
from collection.serializers import CollectionSerializer
from .models import Scenario


class ScenarioSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer

    class Meta:
        model = Scenario
        fields = ['id', 'name', 'collection']
