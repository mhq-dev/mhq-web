from mhq_web.celery import app
from .execute import ScenarioExecution


@app.task
def execute(scenario_id, user_id):
    exe = ScenarioExecution(scenario_id=scenario_id, user_id=user_id)
    exe.execute()
