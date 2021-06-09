from django.db import models


class Module(models.Model):
    scenario = models.ForeignKey('scenario.Scenario', on_delete=models.CASCADE, )
    request = models.ForeignKey('request.Request', on_delete=models.CASCADE, null=True, blank=True)
    x_position = models.FloatField()
    y_position = models.FloatField()

    class Meta:
        db_table = 'module'
