import json

from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from edge.models import Edge
from module.models import Module


def get_default_schedule(self):
    interval = IntervalSchedule.objects.create(
        every=15,
        period=IntervalSchedule.MINUTES)
    return PeriodicTask.objects.create(
        interval=interval,
        name='scenario_' + self.name + '_schedule',
        task='scenario.tasks.execute',
        args=json.dumps([self.id]))


class Scenario(models.Model):
    INTERVALS = 'intervals'
    ONCE = 'once'
    EVERY_DAY = 'every_day'
    DAYS_OF_WEEK = 'days_of_week'
    DAYS_OF_MONTH = 'days_of_week'
    SPECIFIED_DATES = 'specified_dates'

    name = models.CharField(max_length=100)
    collection = models.ForeignKey('collection.Collection', on_delete=models.CASCADE)
    starter_module = models.OneToOneField(Module, on_delete=models.DO_NOTHING, null=True)
    schedule = models.OneToOneField(PeriodicTask, default=get_default_schedule, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ') ' + self.name

    def get_modules(self):
        return Module.objects.all().filter(scenario__id=self.id)

    class Meta:
        db_table = 'scenarios'
