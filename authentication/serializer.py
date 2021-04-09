from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'bio']
