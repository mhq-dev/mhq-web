from edge.models import Edge
from request.managers import RequestExecution
from .signals import scenario_history_signal
from .models import ScenarioHistory
from datetime import datetime


class ScenarioExecution:
    def __init__(self, scenario, user):
        self.scenario = scenario
        self.response_list = []
        self.user = user
        self.path = []

    def check_statement(self, response, edge):
        return True

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
        final_result = None
        stack.append(start)
        while len(stack) > 0:
            module = stack.pop()
            request = module.request
            try:
                response = RequestExecution(request=request, user=self.user, module=module,
                                            scenario_history=scenario_history).execute()
            except Exception as e:
                return e, module
            final_result = response.copy()
            self.response_list.append((module.id, response))
            edges = Edge.objects.all().filter(source=module)
            for e in edges:
                if self.check_statement(response, e):
                    stack.append(e.dist)
                    break
        # end of scenario execution
        scenario_history.end_execution_time = datetime.now()
        scenario_history.save()
        print(
            f' end time {scenario_history.end_execution_time}, start time : {scenario_history.start_request_time}')

        return final_result
