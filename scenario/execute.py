from edge.models import Edge
from request.views import RequestViewSet

class Execution:
    def __init__(self, scenario):
        self.scenario = scenario

    def check_statement(self):
        return True

    def execute(self):
        start = self.scenario.starter_module
        path = []
        stack = []
        stack.append(start)
        while len(stack) > 0:
            tmp = stack.pop()

            path.append(tmp)
            neighbours = Edge.objects.all().filter(source=tmp)
            for n in neighbours:
                if self.check_statement():
                    path.append(n.dist)
                    break
        results = []
        for m in path:
            results.append(m.run_module())
        return results
