from django.db import models


class Request(models.Model):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

    collection = models.ForeignKey('collection.Collection', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    http_method = models.CharField(max_length=255, default=GET)
    url = models.CharField(max_length=255)
    body = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'requests'
