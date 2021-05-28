from django.db import models


class Condition(models.Model):
    EQUAL = 'equal'
    EXIST = 'exist'
    START_WITH = 'start_with'
    CONTAINS = 'contains'
    CONDITIONS = [EQUAL, EXIST, START_WITH, CONTAINS]

    operator = models.CharField(default=EQUAL, max_length=250)
    statement = models.ForeignKey('edge.Statement', on_delete=models.CASCADE)
    first = models.CharField(max_length=250)
    second = models.CharField(max_length=250)

    class Meta:
        db_table = 'conditions'
