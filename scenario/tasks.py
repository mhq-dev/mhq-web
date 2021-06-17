from mhq_web.celery import app
from .execute import ScenarioExecution


@app.task
def execute(scenario_id, user_id, scenario_history_id=None):
    exe = ScenarioExecution(scenario_id=scenario_id, user_id=user_id, scenario_history_id=scenario_history_id)
    exe.execute()
