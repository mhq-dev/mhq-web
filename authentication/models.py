import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    # get filename
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join('pictures/avatar/', filename)


class User(AbstractUser):
    avatar = models.ImageField(upload_to=wrapper, null=True, blank=True)
    bio = models.CharField(max_length=255, default=None, null=True, blank=True)

    REQUIRED_FIELDS = ['email', ]

    class Meta:
        db_table = 'users'

    def get_user_followers(self):
        l = UserFollow.objects.all().filter(followed=self)
        return [u.follower for u in l]

    def get_user_followings(self):
        l = UserFollow.objects.all().filter(follower=self)
        return [u.followed for u in l]

    def __str__(self):
        return self.username


class UserFollow(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followed')

    class Meta:
        db_table = 'follows'
        unique_together = ('follower', 'followed')
