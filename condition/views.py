from .models import Condition
from rest_framework import viewsets
from .serializers import ConditionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http.response import JsonResponse


class ConditionViewSet(viewsets.ModelViewSet):
    serializer_class = ConditionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Condition.objects.all()

    def get_available_conditions(self, request, *args, **kwargs):
        return Response(Condition.CONDITIONS, status=status.HTTP_200_OK)

    def get_condition_of_statement(self, request, *args, **kwargs):
        return JsonResponse(
            ConditionSerializer(Condition.objects.all().filter(statement_id=kwargs.get('statement_id')),
                                many=True).data,
            safe=False, status=status.HTTP_200_OK)
