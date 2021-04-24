from rest_framework import serializers
from .models import Scenario
from collection.models import Collection


class CollectionScenarioSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return Collection.objects.get(pk=data)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['name', 'type']


class ScenarioSerializer(serializers.ModelSerializer):
    collection = CollectionScenarioSerializer(required=False)

    class Meta:
        model = Scenario
        fields = ['id', 'name', 'collection']
