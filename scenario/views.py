from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .serializers import ScenarioSerializer
from rest_framework import viewsets, status
from .models import Scenario
from collection.models import UserCollection


class ScenarioViewSets(viewsets.ModelViewSet):
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Scenario.objects.all()

    def list(self, request, *args, **kwargs):
        collection_id = kwargs['id']
        username = kwargs['username']
        if collection_id is None or username is None:
            return JsonResponse({'error ': 'give me the username and collection id'},
                                status=status.HTTP_400_BAD_REQUEST)

        u = UserCollection.objects.filter(user=request.user, collection_id=id).first()
        obj = self.get_queryset().get(collection=u.collection)
        return JsonResponse(ScenarioSerializer(obj).data, safe=False, status=status.HTTP_200_OK)
