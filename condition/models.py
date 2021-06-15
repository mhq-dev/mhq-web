from django.db import models


class Condition(models.Model):
    EQUAL = 'equal'
    EXIST = 'exist'
    START_WITH = 'start_with'
    CONTAINS = 'contains'
    CONDITIONS = [EQUAL, EXIST, START_WITH, CONTAINS]

    STR = 'str'
    NUM = 'num'
    TIMESTAMP = 'timestamp'
    BODY = 'body'
    STATUS_CODE = 'status_code'
    TOKENS = [STR, NUM, TIMESTAMP, BODY, STATUS_CODE]

    operator = models.CharField(default=EQUAL, max_length=255, blank=True)
    statement = models.ForeignKey('edge.Statement', on_delete=models.CASCADE, blank=True)
    first_token = models.CharField(max_length=255, default=STR, blank=True)
    first = models.CharField(max_length=255, null=True, blank=True)
    second_token = models.CharField(max_length=255, default=STR, blank=True)
    second = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'conditions'
