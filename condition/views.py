from django.shortcuts import render
from .models import Condition
from rest_framework import viewsets
from .serializers import ConditionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class ConditionViewSet(viewsets.ModelViewSet):
    serializer_class = ConditionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Condition.objects.all()

    def get_available_conditions(self, request, *args, **kwargs):
        return Response(Condition.CONDITIONS, status=status.HTTP_200_OK)
