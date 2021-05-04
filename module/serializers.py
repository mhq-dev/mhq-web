from rest_framework import serializers
from .models import Module


class ModuleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
