from mhq_web.celery import app
from .models import Scenario
from django.shortcuts import get_object_or_404
from edge.models import Edge, Statement


def check_statement(edge):
    return True


@app.task
def execute_scenario(scenario_id):
    pass