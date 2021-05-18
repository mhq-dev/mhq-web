from rest_framework import serializers
from .models import Scenario
from collection.models import Collection
from module.models import Module
from edge.models import Edge


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


class SpecificModuleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='request.name', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'x_position', 'y_position']


class SpecificEdgeSerializer(serializers.ModelSerializer):
    source = SpecificModuleSerializer(source='get_source', read_only=True)
    dist = SpecificModuleSerializer(source='get_dist', read_only=True)

    class Meta:
        model = Edge
        fields = ['source', 'dist']
