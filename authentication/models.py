from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
