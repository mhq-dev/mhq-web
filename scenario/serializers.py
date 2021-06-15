from rest_framework import serializers
from .models import Scenario, ScenarioSchedule
from collection.models import Collection
from module.models import Module
from edge.models import Edge
from .models import ScenarioHistory


class CollectionScenarioSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return Collection.objects.get(pk=data)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['name', 'type']


class SpecificModuleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='request.name', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'request', 'name', 'x_position', 'y_position']


class SpecificEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['id', 'source', 'dist']


class ScenarioSerializer(serializers.ModelSerializer):
    collection = CollectionScenarioSerializer(required=False)
    edges = SpecificEdgeSerializer(source='get_edges', many=True, read_only=True, required=False)
    nodes = SpecificModuleSerializer(source='get_modules', many=True, read_only=True, required=False)

    class Meta:
        model = Scenario
        fields = ['id', 'name', 'collection', 'starter_module', 'edges', 'nodes']


class LiteScenarioSerializer(serializers.ModelSerializer):
    collection = CollectionScenarioSerializer(required=False)

    class Meta:
        model = Scenario
        fields = ['id', 'name', 'collection']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioSchedule
        fields = ['type', 'enable', 'minutes', 'date',
                  'time', 'days', 'months',
                  'start_date_time', 'expired_date_time']
        extra_kwargs = {'type': {'required': True}}

    def validate_type(self, s_type):
        if s_type not in [ScenarioSchedule.INTERVALS, ScenarioSchedule.ONCE, ScenarioSchedule.EVERY_DAY,
                          ScenarioSchedule.DAYS_OF_WEEK, ScenarioSchedule.DAYS_OF_MONTH,
                          ScenarioSchedule.SPECIFIED_DATES]:
            raise serializers.ValidationError("your schedule type is not valid!")
        return s_type

    def validate_minutes(self, minutes):
        if minutes is None:
            return minutes
        if minutes < 15:
            raise serializers.ValidationError("Minute must be higher than or equal to 15!")
        return minutes

    def validate_days(self, days):
        if days is None:
            return days
        days_list = days.split(',')
        for d in days_list:
            try:
                d = int(d)
            except ValueError:
                raise serializers.ValidationError("days is not valid!")
            if self.initial_data['type'] == ScenarioSchedule.DAYS_OF_MONTH and (d > 31 or d < 1):
                raise serializers.ValidationError("days is not valid!")
            if self.initial_data['type'] == ScenarioSchedule.DAYS_OF_WEEK and (d > 6 or d < 0):
                raise serializers.ValidationError("days is not valid!")
        return days

    def validate_months(self, months):
        if months is None:
            return months
        months_list = months.split(',')
        for m in months_list:
            try:
                m = int(m)
            except ValueError:
                raise serializers.ValidationError("months is not valid!")
            if m > 11 or m < 0:
                raise serializers.ValidationError("months is not valid!")
        return months


class ScenarioHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioHistory
        fields = ['name', 'user', 'scenario', 'collection',
                  'start_request_time', 'end_execution_time', 'schedule', ]
