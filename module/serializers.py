from rest_framework import serializers
from .models import Module
from request.models import Request
from scenario.models import Scenario


class ScenarioModuleSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return Scenario.objects.get(pk=data)

    class Meta:
        model = Scenario
        fields = ['id', 'name', ]
        read_only_fields = ['name', ]


class RequestModuleSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return Request.objects.get(pk=data)

    class Meta:
        model = Request
        fields = ['id', 'name', 'http_method', 'url', ]
        read_only_fields = ['name', 'http_method', 'url', ]


class ModuleSerializer(serializers.ModelSerializer):
    scenario = ScenarioModuleSerializer(required=False)
    request = RequestModuleSerializer(required=False)

    class Meta:
        model = Module
        fields = ['id', 'scenario', 'request', 'x_position', 'y_position']

    def validate_request(self, request):
        scenario = None
        if self.instance is not None:
            scenario = self.instance.scenario
        if 'scenario' in self.initial_data:
            scenario = Scenario.objects.get(id=self.initial_data['scenario'])
        if scenario.collection != request.collection:
            raise serializers.ValidationError("request and scenario should be in the same collection!")
        return request
