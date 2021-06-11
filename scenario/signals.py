from django.dispatch import Signal
from django.dispatch import receiver
from .models import Scenario

scenario_run_finished = Signal(providing_args=['request', 'response'])


@receiver(scenario_run_finished)
def add_scenario_history(sender, **kwargs):
    print("Request History Saved")
