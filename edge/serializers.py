from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Edge


class EdgeCreateSerializer(ModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'

    def validate(self, attrs):
        if attrs['source'] == attrs['dist']:
            raise ValidationError('Not Allowed to have cycle .')
        return super(EdgeCreateSerializer, self).validate(attrs)