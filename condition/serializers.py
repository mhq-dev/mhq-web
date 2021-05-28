from rest_framework.serializers import ModelSerializer
from .models import Condition


class ConditionSerializer(ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'
