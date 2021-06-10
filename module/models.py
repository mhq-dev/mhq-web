from django.db import models


class Module(models.Model):
    scenario = models.ForeignKey('scenario.Scenario', on_delete=models.CASCADE, blank=True)
    request = models.ForeignKey('request.Request', on_delete=models.CASCADE, null=True, blank=True)
    x_position = models.FloatField(default=0.0, blank=True)
    y_position = models.FloatField(default=0.0, blank=True)

    class Meta:
        db_table = 'module'
