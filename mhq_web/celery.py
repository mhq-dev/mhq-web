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


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=0),
        test.s('day of week 0 hour 10:10'),
    )
    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=1),
        test.s('day of week 1 hour 10:10'),
    )
    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=2),
        test.s('day of week 2 hour 10:10'),
    )
    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=3),
        test.s('day of week 3 hour 10:10'),
    )
    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=4),
        test.s('day of week 4 hour 10:10'),
    )
    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=5),
        test.s('day of week 5 hour 10:10'),
    )

    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=6),
        test.s('day of week 6 hour 10:10'),
    )

    sender.add_periodic_task(
        crontab(hour=10, minute=10, day_of_week=7),
        test.s('day of week 7 hour 10:10'),
    )

    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=0),
        test.s('day of week 0 hour 14:40'),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=1),
        test.s('day of week 1 hour 14:40'),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=2),
        test.s('day of week 2 hour 14:40'),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=3),
        test.s('day of week 3 hour 14:40'),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=4),
        test.s('day of week 4 hour 14:40'),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=5),
        test.s('day of week 5 hour 14:40'),
    )

    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=6),
        test.s('day of week 6 hour 14:40'),
    )

    sender.add_periodic_task(
        crontab(hour=14, minute=40, day_of_week=7),
        test.s('day of week 7 hour 14:40'),
    )



@app.task
def test(arg):
    print(arg)
