from rest_framework import serializers
from .models import Module
from request.models import Request
from scenario.models import Scenario


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class ModuleScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


class RequestModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'name', 'http_method', 'url', ]


class ModuleCompleteSerializer(serializers.ModelSerializer):
    scenario = ModuleScenarioSerializer(data='scenario', required=False)
    request = RequestModuleSerializer(data='request', read_only=True, required=False)

    class Meta:
        model = Module
        fields = ['id', 'scenario', 'request', ]
