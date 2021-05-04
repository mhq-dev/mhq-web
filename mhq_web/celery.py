import calendar
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab
from django.http import HttpResponse
from requests import Response
# from rest_framework.decorators import api_view

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mhq_web.settings')

app = Celery('mhq_web')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s(), name='add every 10')
    #
    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s(), expires=10)
    #
    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=15, minute=7),
    #     test.s('fuuuuuccckkkk yoooouuuu'),
    # )
    pass


@app.task
def test():
    dt_string = crontab().now().strftime("%d/%m/%Y %H:%M:%S")
    print('fuck')
    print("date and time =", dt_string)
    print('weekday: ', crontab().now().weekday(), calendar.day_name[crontab().now().weekday()])


# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.add',
#         'schedule': 30.0,
#         'args': (16, 16)
#     },
# }

#
# @api_view(['GET'])
# def test_celery(request):
#     print('hi')
#     return HttpResponse()
