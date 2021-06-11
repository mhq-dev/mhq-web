from edge.models import Edge
from request.managers import RequestExecution


class Execution:
    def __init__(self, scenario):
        self.scenario = scenario
        self.response_list = []
        self.path = []

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
                response = RequestExecution(request=request).execute()
            except Execution as e:
                return e, module
            self.response_list.append((module.id, response))
            responses.append(response)
            self.path.append(module.id)
            edges = Edge.objects.all().filter(source=module)
            for e in edges:
                if self.check_statement(response, e.dist):
                    stack.append(e.dist)
                    break
        return responses.pop()
