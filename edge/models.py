from django.db import models


class Edge(models.Model):
    source = models.ForeignKey('module.Module', on_delete=models.CASCADE, related_name='source')
    dist = models.ForeignKey('module.Module', on_delete=models.CASCADE, related_name='dist')

    class Meta:
        unique_together = ('source', 'dist')
        db_table = 'edges'

    def get_source(self):
        return self.source

    def get_dist(self):
        return self.dist