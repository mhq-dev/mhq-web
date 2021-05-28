from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import ScenarioSerializer
from rest_framework import viewsets, status
from .models import Scenario
from collection.models import Collection
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from .permissions import ScenarioPermission
from edge.models import Edge
from module.models import Module
from .serializers import SpecificEdgeSerializer


class ScenarioViewSets(viewsets.ModelViewSet):
    serializer_class = ScenarioSerializer
    permission_classes = [ScenarioPermission, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Scenario.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                                 | Q(collection__usercollection__user=self.request.user)).distinct()
        return Scenario.objects.all().filter(collection__type=Collection.PUBLIC)

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        collection = get_object_or_404(Collection, id=collection_id)
        scenarios = Scenario.objects.filter(collection=collection)
        return JsonResponse(ScenarioSerializer(scenarios, many=True).data, safe=False, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        scenario_id = kwargs.get('scenario_id')
        collection = get_object_or_404(Collection, id=collection_id)
        scenario = get_object_or_404(Scenario, collection=collection, id=scenario_id)
        edges = Edge.objects.all().filter(source__scenario=scenario)
        node_num = len(Module.objects.all().filter(scenario=scenario))
        return JsonResponse({'node_count': node_num,
                             'edges': SpecificEdgeSerializer(edges, many=True).data}, safe=False,
                            status=status.HTTP_200_OK)


class StarterModuleViewSet(viewsets.ViewSet):

    def set_starter_module(self, request, pk, module_id):
        scenario = get_object_or_404(Scenario, id=pk)
        module = get_object_or_404(scenario.get_modules(), id=module_id)
        scenario.starter_module = module
        return Response({'msg': 'set successfully'}, status=status.HTTP_200_OK)

    def set_schedule(self, request, pk, schedule_type):
        scenario = get_object_or_404(Scenario, id=pk)
        schedule = scenario.schedule
        if schedule_type == Scenario.INTERVALS:
            pass
        elif schedule_type == Scenario.ONCE:
            pass
        elif schedule_type == Scenario.EVERY_DAY:
            pass
        elif schedule_type == Scenario.DAYS_OF_WEEK:
            pass
        elif schedule_type == Scenario.DAYS_OF_MONTH:
            pass
        elif schedule_type == Scenario.SPECIFIED_DATES:
            pass
        else:
            return Response({'msg': 'schedule type is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
