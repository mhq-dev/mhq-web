from rest_framework import serializers

from collection.models import Collection, UserCollection


class UserCollectionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserCollection
        fields = ['user', 'role']


class CollectionSerializer(serializers.ModelSerializer):
    users = UserCollectionSerializer(source='get_user_collections', many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'type', 'name', 'users']
