from authentication.models import User
from edge.managers import EdgeManager
from edge.models import Edge
from request.managers import RequestExecution
from .models import ScenarioHistory, Scenario
from datetime import datetime


class ScenarioExecution:
    def __init__(self, scenario_id, user_id, scenario_history_id=None):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.user = User.objects.get(id=user_id)
        if scenario_history_id:
            self.scenario_history = ScenarioHistory.objects.get(
                id=scenario_history_id
            )
        else:
            self.scenario_history = ScenarioHistory.objects.create(
                name=self.scenario.name,
                user=self.user,
                scenario=self.scenario,
                collection=self.scenario.collection,
                schedule=str(self.scenario.schedule.periodic_task)
            )
            self.scenario_history.save()

    def finish(self):
        self.scenario_history.end_execution_time = datetime.now()
        self.scenario_history.save()

    def execute(self):
        self.scenario_history.status = ScenarioHistory.PROGRESS
        self.scenario_history.save()

        start = self.scenario.starter_module
        stack = [start]
        while len(stack) > 0:
            module = stack.pop()
            request = module.request
            try:
                RequestExecution(request=request, user=self.user, module=module,
                                 scenario_history=self.scenario_history).execute()
            except Exception:
                self.scenario_history.status = ScenarioHistory.FAILED
                self.finish()
                return

            edges = Edge.objects.all().filter(source=module)
            for e in edges:
                if EdgeManager(e, self.scenario_history).check():
                    stack.append(e.dist)

        self.scenario_history.status = ScenarioHistory.COMPLETED
        self.finish()

        print(f'end time {self.scenario_history.end_execution_time}, ',
              f'start time : {self.scenario_history.start_execution_time}')

        return
