from django.http import JsonResponse
from .serializers import ScenarioSerializer
from rest_framework import viewsets, status
from .models import Scenario
from collection.models import Collection
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from .permissions import ScenarioPermission


class ScenarioViewSets(viewsets.ModelViewSet):
    serializer_class = ScenarioSerializer
    permission_classes = [ScenarioPermission, ]

    def get_queryset(self):
        return Scenario.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                             | Q(collection__usercollection__user=self.request.user)).distinct()

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        collection = get_object_or_404(Collection, id=collection_id)
        scenarios = Scenario.objects.filter(collection=collection)
        return JsonResponse(ScenarioSerializer(scenarios, many=True).data, safe=False, status=status.HTTP_200_OK)
