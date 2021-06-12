from edge.models import Edge
from request.managers import RequestExecution
from .signals import scenario_history_signal
from .models import ScenarioHistory, Scenario
from datetime import datetime


class ScenarioExecution:
    def __init__(self, scenario_id, user_id):
        self.scenario = Scenario.objects.get(id=scenario_id)
        self.response_list = []
        self.user = User.objects.get(id=user_id)

    def finish_scenario_execution(self, scenario_history):
        scenario_history.end_execution_time = datetime.now()
        scenario_history.save()

    def execute(self):

        # create scenario_history object
        date_time = datetime.now()
        scenario_history = ScenarioHistory.objects.create(name=self.scenario.name,
                                                          user=self.user,
                                                          scenario=self.scenario,
                                                          collection=self.scenario.collection,
                                                          end_execution_time=None,
                                                          schedule=str(self.scenario.schedule.periodic_task))

        scenario_history.save()

        start = self.scenario.starter_module
        stack = []
        stack.append(start)
        while len(stack) > 0:
            module = stack.pop()
            request = module.request
            try:
                response = RequestExecution(request=request, user=self.user, module=module,
                                            scenario_history=scenario_history).execute()
            except Exception:
                self.finish_scenario_execution(scenario_history=scenario_history)
                return
            self.response_list.append((module.id, response))
            edges = Edge.objects.all().filter(source=module)
            for e in edges:
                if EdgeManager(e).check():
                    stack.append(e.dist)
                    break

        # end of scenario execution
        self.finish_scenario_execution(scenario_history=scenario_history)
        print(
            f' end time {scenario_history.end_execution_time}, start time : {scenario_history.start_request_time}')

        return
