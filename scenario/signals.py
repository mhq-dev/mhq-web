from django.dispatch import Signal
from django.dispatch import receiver
from .models import Scenario, ScenarioHistory

scenario_history_signal = Signal(
    providing_args=['user', 'name', 'scenario'])


@receiver(scenario_history_signal)
def add_scenario_history(sender, **kwargs):
    user = kwargs.get('user')
    name = kwargs.get('name')
    scenario = kwargs.get('scenario')
    # exe_time = kwargs.get('execution_time')
    # schedule = kwargs.get('schedule')

    ScenarioHistory.objects.create(name=name,
                                   user=user,
                                   scenario=scenario,
                                   collection=scenario.collection,
                                   schedule=str(scenario.schedule)).save()
