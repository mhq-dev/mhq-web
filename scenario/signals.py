from django.dispatch import Signal
from django.dispatch import receiver
from .models import Scenario, ScenarioHistory

scenario_run_finished = Signal(
    providing_args=['user', 'response', 'name', 'scenario', 'order'])


@receiver(scenario_run_finished)
def add_scenario_history(sender, **kwargs):
    user = kwargs.get('user')
    response = kwargs.get('response')
    name = kwargs.get('name')
    scenario = kwargs.get('scenario')
    order = kwargs.get('order')
    # exe_time = kwargs.get('execution_time')
    # schedule = kwargs.get('schedule')

    ScenarioHistory.objects.create(name=name,
                                   user=user,
                                   scenario=scenario,
                                   order=order,
                                   collection=scenario.collection).save()
