from condition.managers import ConditionManager


class EdgeManager:
    def __init__(self, edge, scenario_history=None, parent_response=None):
        self.edge = edge
        self.scenario_history = scenario_history
        self.parent_response = parent_response

    def check(self):
        statements = self.edge.get_statements()

        if len(statements) == 0:
            return True

        result = False
        for statement in statements:
            result = result or self.check_statement(statement)

        return result

    def check_statement(self, statement):
        conditions = statement.get_conditions()

        result = True
        for condition in conditions:
            result = result and ConditionManager(condition.id, self.parent_response).check()

        return result
