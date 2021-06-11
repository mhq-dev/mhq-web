from mhq_web.celery import app
from .models import Scenario
from django.shortcuts import get_object_or_404
from .execute import Execution
from request.managers import RequestExecution
import requests


@app.task
def execute_scenario():
    res = requests.post('https://60c1f3514f7e880017dc0e65.mockapi.io/scenario')
    print(res)
    # exe = Execution(scenario=scenario)
    # response = exe.execute()
    # if isinstance(response, Exception):
    #     return str(response)
    # return response
