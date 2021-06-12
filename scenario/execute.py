from edge.models import Edge
from request.managers import RequestExecution
from .signals import scenario_run_finished


class ScenarioExecution:
    def __init__(self, scenario, user):
        self.scenario = scenario
        self.response_list = []
        self.path = []
        self.user = user

    def check_statement(self, response, edge):
        return True

    def execute(self):
        start = self.scenario.starter_module
        stack = []
        responses = []
        stack.append(start)
        while len(stack) > 0:
            module = stack.pop()
            request = module.request
            try:
                response, req_id = RequestExecution(request=request, user=self.user).execute()
            except Exception as e:
                return e, module
            self.response_list.append((module.id, response))
            responses.append(response)
            self.path.append(req_id)
            edges = Edge.objects.all().filter(source=module)
            for e in edges:
                if self.check_statement(response, e):
                    stack.append(e.dist)
                    break
        last_response = responses.pop()
        scenario_run_finished.send(sender=None, user=self.user, response=last_response, name=self.scenario.name,
                                   scenario=self.scenario, order=self.path)
        return last_response
