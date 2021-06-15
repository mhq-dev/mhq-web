import datetime

from condition.models import Condition


class ConditionManager:
    def __init__(self, condition_id):
        self.condition = Condition.objects.get(id=condition_id)

    def str(self, s):
        return str(s)

    def num(self, n):
        return float(n)

    def timestamp(self, t):
        datetime.datetime.strptime(t, "%d/%m/%Y")

    def body(self, b):
        pass

    def status_code(self, sc):
        pass

    def equal(self, var1, var2):
        return var1 == var2

    def exist(self, var1, nothing):
        pass

    def start_with(self, var1, var2):
        return str(var1).startswith(str(var2))

    def contains(self, var1, var2):
        return str(var2) in str(var1)

    def check(self):
        token_types = {Condition.STR: self.str, Condition.NUM: self.num,
                       Condition.TIMESTAMP: self.timestamp, Condition.BODY: self.body,
                       Condition.STATUS_CODE: self.status_code}

        condition_types = {Condition.EQUAL: self.equal, Condition.EXIST: self.exist,
                           Condition.START_WITH: self.start_with, Condition.CONTAINS: self.contains}

        var1 = token_types[self.condition.first_token](self.condition.first)
        var2 = token_types[self.condition.second_token](self.condition.second)

        return condition_types[self.condition.operator](var1, var2)
