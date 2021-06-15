from django.db import models
from condition.models import Condition


class Edge(models.Model):
    source = models.ForeignKey('module.Module', on_delete=models.CASCADE, related_name='source', blank=True)
    dist = models.ForeignKey('module.Module', on_delete=models.CASCADE, related_name='dist', blank=True)

    def get_statements(self):
        return Statement.objects.all().filter(edge__id=self.id)

    class Meta:
        unique_together = ('source', 'dist')
        db_table = 'edges'


class Statement(models.Model):
    edge = models.ForeignKey(Edge, on_delete=models.CASCADE, related_name='statement_of')

    def get_conditions(self):
        return Condition.objects.all().filter(statement__id=self.id)

    class Meta:
        db_table = 'statements'
