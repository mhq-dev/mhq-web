from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    avatar = models.ImageField(upload_to='pictures/avatar/', null=True, blank=True)
    bio = models.CharField(max_length=255, default=None, null=True, blank=True)

    REQUIRED_FIELDS = ['email', ]

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
