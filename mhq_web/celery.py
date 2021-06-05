import calendar
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

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


@app.task
def print_date():
    dt_string = crontab().now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    print('weekday: ', crontab().now().weekday(), calendar.day_name[crontab().now().weekday()])
