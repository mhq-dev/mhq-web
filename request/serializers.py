from rest_framework import serializers

from collection.models import Collection
from request.models import Request


class CollectionLiteSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        return Collection.objects.get(pk=data)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'type']
        read_only_fields = ['name', 'type']


class RequestFullSerializer(serializers.ModelSerializer):
    collection = CollectionLiteSerializer(required=False)

    class Meta:
        model = Request
        fields = ['id', 'name', 'http_method', 'url', 'body', 'collection']
