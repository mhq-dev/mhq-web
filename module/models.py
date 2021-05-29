from django.db import models
from edge.models import Edge


class Module(models.Model):
    scenario = models.ForeignKey('scenario.Scenario', on_delete=models.CASCADE, )
    request = models.ForeignKey('request.Request', on_delete=models.CASCADE, )
    x_position = models.FloatField()
    y_position = models.FloatField()

    class Meta:
        db_table = 'module'

    def get_neighbours(self):
        near = Edge.objects.all().filter(source=self)
        return [n.dist for n in near]

    def run_module(self):
        print('Hello')
