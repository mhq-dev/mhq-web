from django.http import JsonResponse
from django_celery_beat.models import IntervalSchedule, ClockedSchedule, CrontabSchedule
from rest_framework.response import Response

from .serializers import ScenarioSerializer, ScheduleSerializer, LiteScenarioSerializer
from rest_framework import viewsets, status
from .models import Scenario, ScenarioSchedule, get_default_periodic_task
from collection.models import Collection
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from .permissions import ScenarioPermission


class ScenarioViewSets(viewsets.ModelViewSet):
    serializer_class = ScenarioSerializer
    permission_classes = [ScenarioPermission, ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Scenario.objects.all().filter(Q(collection__type=Collection.PUBLIC)
                                                 | Q(collection__usercollection__user=self.request.user)).distinct()
        return Scenario.objects.all().filter(collection__type=Collection.PUBLIC)

    def get_collection_queryset(self):
        if self.request.user.is_authenticated:
            return Collection.objects.all().filter(Q(type=Collection.PUBLIC)
                                                   | Q(usercollection__user=self.request.user)).distinct()
        return Collection.objects.all().filter(Q(type=Collection.PUBLIC))

    def perform_create(self, serializer):
        scenario = serializer.save()
        scenario.schedule = ScenarioSchedule.objects.create(periodic_task=get_default_periodic_task(scenario))
        scenario.save()

    def list(self, request, *args, **kwargs):
        collection_id = kwargs.get('collection_id')
        collection = get_object_or_404(self.get_collection_queryset(), id=collection_id)
        scenarios = Scenario.objects.filter(collection=collection)
        return JsonResponse(LiteScenarioSerializer(scenarios, many=True).data, safe=False, status=status.HTTP_200_OK)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return ScenarioSchedule.objects.all()

    def get_schedule(self, request, pk):
        scenario = get_object_or_404(Scenario, id=pk)
        schedule = scenario.schedule
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)

    def set_schedule(self, request, pk):
        scenario = get_object_or_404(Scenario, id=pk)
        schedule = scenario.schedule
        serializer = self.get_serializer(schedule, data=request.data)
        serializer.is_valid(raise_exception=True)
        periodic_task = schedule.periodic_task

        if serializer.validated_data['type'] == ScenarioSchedule.INTERVALS:
            if 'minutes' not in serializer.validated_data:
                return Response({'msg': 'intervals needs minutes'}, status=status.HTTP_400_BAD_REQUEST)
            periodic_task.interval, temp = IntervalSchedule.objects.get_or_create(
                every=serializer.validated_data['minutes'],
                period=IntervalSchedule.MINUTES
            )
            periodic_task.one_off = False
            periodic_task.clocked = None
            periodic_task.crontab = None
        elif serializer.validated_data['type'] == ScenarioSchedule.ONCE:
            if 'date' not in serializer.validated_data:
                return Response({'msg': 'once needs date'}, status=status.HTTP_400_BAD_REQUEST)
            periodic_task.clocked, temp = ClockedSchedule.objects.get_or_create(
                clocked_time=serializer.validated_data['date']
            )
            periodic_task.one_off = True
            periodic_task.interval = None
            periodic_task.crontab = None
        elif serializer.validated_data['type'] == ScenarioSchedule.EVERY_DAY:
            if 'time' not in serializer.validated_data:
                return Response({'msg': 'every_day needs time'}, status=status.HTTP_400_BAD_REQUEST)
            periodic_task.crontab, temp = CrontabSchedule.objects.get_or_create(
                minute=serializer.validated_data['time'].minute,
                hour=serializer.validated_data['time'].hour
            )
            periodic_task.one_off = False
            periodic_task.interval = None
            periodic_task.clocked = None
        elif serializer.validated_data['type'] == ScenarioSchedule.DAYS_OF_WEEK:
            if 'time' not in serializer.validated_data or 'days' not in serializer.validated_data:
                return Response({'msg': 'days_of_week needs time and days'}, status=status.HTTP_400_BAD_REQUEST)
            periodic_task.crontab, temp = CrontabSchedule.objects.get_or_create(
                minute=serializer.validated_data['time'].minute,
                hour=serializer.validated_data['time'].hour,
                day_of_week=serializer.validated_data['days']
            )
            periodic_task.one_off = False
            periodic_task.interval = None
            periodic_task.clocked = None
        elif serializer.validated_data['type'] == ScenarioSchedule.DAYS_OF_MONTH:
            if 'time' not in serializer.validated_data or 'days' not in serializer.validated_data:
                return Response({'msg': 'days_of_month needs time and days'}, status=status.HTTP_400_BAD_REQUEST)
            periodic_task.crontab, temp = CrontabSchedule.objects.get_or_create(
                minute=serializer.validated_data['time'].minute,
                hour=serializer.validated_data['time'].hour,
                day_of_month=serializer.validated_data['days']
            )
            periodic_task.one_off = False
            periodic_task.interval = None
            periodic_task.clocked = None
        elif serializer.validated_data['type'] == ScenarioSchedule.SPECIFIED_DATES:
            if 'time' not in serializer.validated_data or \
                    'days' not in serializer.validated_data or \
                    'months' not in serializer.validated_data:
                return Response({'msg': 'specified_dates needs time, days and months'},
                                status=status.HTTP_400_BAD_REQUEST)
            periodic_task.crontab, temp = CrontabSchedule.objects.get_or_create(
                minute=serializer.validated_data['time'].minute,
                hour=serializer.validated_data['time'].hour,
                day_of_month=serializer.validated_data['days'],
                month_of_year=serializer.validated_data['months']
            )
            periodic_task.one_off = False
            periodic_task.interval = None
            periodic_task.clocked = None

        if 'start_time' in serializer.validated_data:
            periodic_task.start_time = serializer.validated_data['start_time']
        else:
            periodic_task.start_time = None
        if 'expired_date_time' in serializer.validated_data:
            periodic_task.expired_date_time = serializer.validated_data['expired_date_time']
        else:
            periodic_task.expired_date_time = None

        periodic_task.enabled = serializer.validated_data['enable']
        periodic_task.save()
        serializer.save()
        return Response({'msg': 'set successfully'}, status=status.HTTP_200_OK)
