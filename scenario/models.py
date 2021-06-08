import json

from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from edge.models import Edge
from module.models import Module


class Scenario(models.Model):
    name = models.CharField(max_length=100)
    collection = models.ForeignKey('collection.Collection', on_delete=models.CASCADE)
    starter_module = models.OneToOneField('module.Module',
                                          on_delete=models.DO_NOTHING,
                                          null=True,
                                          blank=True,
                                          related_name='starter_module')
    schedule = models.OneToOneField('ScenarioSchedule', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id) + ') ' + self.name

    def get_modules(self):
        return Module.objects.all().filter(scenario__id=self.id)

    class Meta:
        db_table = 'scenarios'


def get_default_periodic_task(scenario):
    interval, temp = IntervalSchedule.objects.get_or_create(
        every=15,
        period=IntervalSchedule.MINUTES)
    return PeriodicTask.objects.create(
        enabled=False,
        interval=interval,
        name='scenario_' + scenario.name + '_schedule',
        task='scenario.tasks.execute',
        args=json.dumps([scenario.id])
    )


class ScenarioSchedule(models.Model):
    INTERVALS = 'intervals'
    ONCE = 'once'
    EVERY_DAY = 'every_day'
    DAYS_OF_WEEK = 'days_of_week'
    DAYS_OF_MONTH = 'days_of_month'
    SPECIFIED_DATES = 'specified_dates'

    type = models.CharField(max_length=255, default=INTERVALS)
    enable = models.BooleanField(default=False)
    periodic_task = models.OneToOneField(PeriodicTask, on_delete=models.DO_NOTHING)
    minutes = models.IntegerField(null=True, default=15, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    days = models.CharField(max_length=255, null=True, blank=True)
    months = models.CharField(max_length=255, null=True, blank=True)
    start_date_time = models.DateTimeField(null=True, blank=True)
    expired_date_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'scenario_schedules'
