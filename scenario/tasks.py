from mhq_web.celery import app
from .models import Scenario
from django.shortcuts import get_object_or_404
from edge.models import Edge, Statement


def check_statement(edge):
    return True


@app.task
def execute_scenario(scenario_id):
    scenario = get_object_or_404(Scenario, id=scenario_id)
    start = scenario.starter_module
    path = []
    stack = []
    stack.append(start)
    while len(stack) > 0:
        tmp = stack.pop()
        path.append(tmp)
        neighbours = Edge.objects.all().filter(source=tmp)
        for n in neighbours:
            if check_statement(n):
                path.append(n.dist)
                break
    results = []
    for m in path:
        results.append(m.run_module())
    return results