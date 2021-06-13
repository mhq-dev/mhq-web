from authentication.models import User
from edge.managers import EdgeManager
from edge.models import Edge
from request.managers import RequestExecution
from .models import ScenarioHistory, Scenario
from datetime import datetime


class ScenarioExecution:
    def __init__(self, scenario_id, user_id):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.user = User.objects.get(id=user_id)

    def finish(self, scenario_history):
        scenario_history.end_execution_time = datetime.now()
        scenario_history.save()

    def execute(self):

        scenario_history = ScenarioHistory.objects.create(name=self.scenario.name,
                                                          user=self.user,
                                                          scenario=self.scenario,
                                                          collection=self.scenario.collection,
                                                          schedule=str(self.scenario.schedule.periodic_task))
        scenario_history.save()

        start = self.scenario.starter_module
        stack = [start]
        while len(stack) > 0:
            module = stack.pop()
            request = module.request
            try:
                RequestExecution(request=request, user=self.user, module=module,
                                 scenario_history=scenario_history).execute()
            except Exception:
                self.finish(scenario_history=scenario_history)
                return

            edges = Edge.objects.all().filter(source=module)
            for e in edges:
                if EdgeManager(e, scenario_history).check():
                    stack.append(e.dist)
                    break

        self.finish(scenario_history=scenario_history)

        print(f'end time {scenario_history.end_execution_time}, ',
              f'start time : {scenario_history.start_request_time}')

        return
