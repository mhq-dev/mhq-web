from django.db import models
from rest_framework.authtoken.admin import User
# from authentication.models import User


class Collection(models.Model):
    PRIVATE = 'private'
    PUBLIC = 'public'

    type = models.CharField(max_length=255, default=PUBLIC)
    name = models.CharField(max_length=255)

    def get_user_collections(self):
        return UserCollection.objects.all().filter(collection__id=self.id)

    def get_requests(self):
        pass

    def get_scenarios(self):
        pass


class UserCollection(models.Model):
    OWNER = 'owner'
    VISITOR = 'visitor'

    role = models.CharField(max_length=255, default=VISITOR)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
