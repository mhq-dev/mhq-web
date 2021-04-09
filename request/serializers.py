from rest_framework import serializers

from collection.models import Collection
from request.models import Request


class CollectionLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'type']


class RequestFullSerializer(serializers.ModelSerializer):
    collection = CollectionLiteSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'name', 'http_method', 'url', 'body', 'collection']
