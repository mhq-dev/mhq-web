from mhq_web.celery import app
from scenario.models import Scenario


@app.task
def execute(scenario_id):
    scenario = Scenario.objects.get(id=scenario_id)
    print('Hi')
