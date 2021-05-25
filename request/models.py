from django.db import models

from authentication.models import User


class Request(models.Model):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'

    collection = models.ForeignKey('collection.Collection', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, blank=True)
    http_method = models.CharField(max_length=255, default=GET, blank=True)
    url = models.CharField(max_length=255, blank=True)
    body = models.JSONField(null=True, blank=True)

    def get_headers(self):
        return KeyValueContainer.objects.all().filter(request__id=self.id, type=KeyValueContainer.HEADER)

    def get_params(self):
        return KeyValueContainer.objects.all().filter(request__id=self.id, type=KeyValueContainer.PARAM)

    def get_enabled_headers(self):
        return self.get_headers().filter(enable=True)

    def get_enabled_params(self):
        return self.get_params().filter(enable=True)

    def get_form_data(self):
        pass

    class Meta:
        db_table = 'requests'


class KeyValueContainer(models.Model):
    HEADER = 'header'
    PARAM = 'param'

    # TODO add form data
    # FORM_DATA = 'form-data'

    type = models.CharField(max_length=255, default=HEADER)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)


class RequestHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    execution_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True)
    http_method = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    body = models.JSONField(null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)
    params = models.JSONField(null=True, blank=True)
    response = models.JSONField(null=True, blank=True)
