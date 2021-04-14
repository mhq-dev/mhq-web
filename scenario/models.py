from django.db import models
from collection.models import Collection


class Scenario(models.Model):
    name = models.CharField(max_length=100)
    collection = models.ForeignKey(to=Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'scenarios'
