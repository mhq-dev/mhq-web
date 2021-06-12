from mhq_web.celery import app
from .execute import ScenarioExecution


@app.task
def execute(scenario, user):
    exe = ScenarioExecution(scenario=scenario, user=user)
    exe.execute()
