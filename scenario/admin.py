from django.contrib import admin
from .models import Scenario, ScenarioSchedule, ScenarioHistory

admin.site.register(Scenario)
admin.site.register(ScenarioSchedule)
admin.site.register(ScenarioHistory)
