from django.db import models
from authentication.models import User
from request.models import Request


class Collection(models.Model):
    PRIVATE = 'private'
    PUBLIC = 'public'

    type = models.CharField(max_length=255, default=PUBLIC)
    name = models.CharField(max_length=255)

    def get_user_collections(self):
        return UserCollection.objects.all().filter(collection__id=self.id)

    def get_requests(self):
        return Request.objects.all().filter(collection__id=self.id)

    def get_scenarios(self):
        pass

    class Meta:
        db_table = 'collections'


class UserCollection(models.Model):
    OWNER = 'owner'
    VISITOR = 'visitor'

    role = models.CharField(max_length=255, default=VISITOR)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_collections'
