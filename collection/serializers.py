from rest_framework import serializers

from collection.models import Collection, UserCollection
from request.models import Request


class UserCollectionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserCollection
        fields = ['user', 'role']


class RequestLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['name', 'http_method']


class CollectionFullSerializer(serializers.ModelSerializer):
    users = UserCollectionSerializer(source='get_user_collections', many=True, read_only=True)
    requests = RequestLiteSerializer(source='get_requests', many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'type', 'name', 'users', 'requests']
