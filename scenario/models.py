from django.db import models
from edge.models import Edge
from module.models import Module


class Scenario(models.Model):
    name = models.CharField(max_length=100)
    collection = models.ForeignKey('collection.Collection', on_delete=models.CASCADE)

    def get_all_edges(self):
        edges = []
        modules = Module.objects.all().filter(scenario=self)
        for m in modules:
            edges.append((m.source, m.dist))
        return edges

    def __str__(self):
        return str(self.id) + ') ' + self.name

    class Meta:
        db_table = 'scenarios'
