from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User, UserFollow


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'bio']
        read_only_fields = ['username', 'email']


class UserFollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ['follower', 'followed', ]


class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'bio', ]

