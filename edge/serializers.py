from rest_framework import serializers

from condition.models import Condition
from .models import Edge, Statement


class ConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = ['statement', 'operator', 'first_token', 'first', 'second_token', 'second']
        extra_kwargs = {'statement': {'required': False, 'write_only': True}, }


class StatementSerializer(serializers.ModelSerializer):
    conditions = ConditionSerializer(source='get_conditions', many=True)

    class Meta:
        model = Statement
        fields = ['edge', 'conditions']
        extra_kwargs = {'edge': {'required': False, 'write_only': True}, }

    def create(self, validated_data):
        conditions = dict()
        if 'get_conditions' in validated_data:
            conditions = validated_data.pop('get_conditions')

        statement = Statement.objects.create(**validated_data)

        for condition in conditions:
            condition['statement'] = statement.id
            serializer = ConditionSerializer(data=dict(condition))
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return statement

    def update(self, instance, validated_data):

        if 'get_conditions' in validated_data:

            conditions = validated_data.pop('get_conditions')
            condition_instances = instance.get_conditions()

            for i in range(min(len(conditions), len(condition_instances))):
                serializer = ConditionSerializer(instance=condition_instances[i], data=dict(conditions[i]))
                serializer.is_valid(raise_exception=True)
                serializer.save()

            for i in range(min(len(conditions), len(condition_instances)), len(conditions)):
                conditions[i]['statement'] = instance.id
                serializer = ConditionSerializer(data=dict(conditions[i]))
                serializer.is_valid(raise_exception=True)
                serializer.save()

            for i in range(min(len(conditions), len(condition_instances)), len(condition_instances)):
                condition_instances[i].delete()

        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class EdgeSerializer(serializers.ModelSerializer):
    statements = StatementSerializer(source='get_statements', many=True)

    class Meta:
        model = Edge
        fields = ['id', 'source', 'dist', 'statements']
        extra_kwargs = {'source': {'required': False},
                        'dist': {'required': False}, }

    def validate(self, attrs):
        source = None
        dist = None
        if self.instance is not None:
            source = self.instance.source
            dist = self.instance.dist
        if 'source' in self.initial_data:
            source = self.initial_data['source']
        if 'dist' in self.initial_data:
            dist = self.initial_data['dist']

        if source == dist:
            raise serializers.ValidationError('Not Allowed to have loop .')

        return super(EdgeSerializer, self).validate(attrs)

    def create(self, validated_data):
        statements = dict()
        if 'get_statements' in validated_data:
            statements = validated_data.pop('get_statements')

        edge = Edge.objects.create(**validated_data)

        for statement in statements:
            statement['conditions'] = statement.pop('get_conditions')
            statement['edge'] = edge.id
            serializer = StatementSerializer(data=dict(statement))
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return edge

    def update(self, instance, validated_data):

        if 'get_statements' in validated_data:

            statements = validated_data.pop('get_statements')
            statement_instances = instance.get_statements()

            for i in range(min(len(statements), len(statement_instances))):
                statements[i]['conditions'] = statements[i].pop('get_conditions')
                serializer = StatementSerializer(instance=statement_instances[i], data=dict(statements[i]))
                serializer.is_valid(raise_exception=True)
                serializer.save()

            for i in range(min(len(statements), len(statement_instances)), len(statements)):
                statements[i]['conditions'] = statements[i].pop('get_conditions')
                statements[i]['edge'] = instance.id
                serializer = StatementSerializer(data=dict(statements[i]))
                serializer.is_valid(raise_exception=True)
                serializer.save()

            for i in range(min(len(statements), len(statement_instances)), len(statement_instances)):
                statement_instances[i].delete()

        instance = super().update(instance, validated_data)
        instance.save()
        return instance
