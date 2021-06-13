from condition.managers import ConditionManager


class EdgeManager:
    def __init__(self, edge, scenario_history):
        self.edge = edge
        self.scenario_history = scenario_history

    def check(self):
        statements = self.edge.get_statements()

        result = True
        for statement in statements:
            result = result or self.check_statement(statement)

        return result

    def check_statement(self, statement):
        conditions = statement.get_conditions()

        result = True
        for condition in conditions:
            result = result and ConditionManager(condition.id).check()

        return result