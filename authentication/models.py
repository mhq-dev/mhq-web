from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    name = models.CharField(max_length=255, default=None)
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
