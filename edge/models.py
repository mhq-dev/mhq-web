from django.db import models
from condition.models import Condition


class Edge(models.Model):
    source = models.ForeignKey('module.Module', on_delete=models.CASCADE, related_name='source')
    dist = models.ForeignKey('module.Module', on_delete=models.CASCADE, related_name='dist')

    def get_statements(self):
        return Statement.objects.all().filter(edge__id=self.id)

    class Meta:
        unique_together = ('source', 'dist')
        db_table = 'edges'


class Statement(models.Model):
    name = models.CharField(max_length=150, blank=True)
    edge = models.ForeignKey(Edge, on_delete=models.CASCADE, related_name='statement_of')

    class Meta:
        db_table = 'statements'

    def get_conditions(self):
        return Condition.objects.all().filter(statement__=self.id)
