from django.db import models
from authentication.models import User
from request.models import Request
from scenario.models import Scenario


class Collection(models.Model):
    PRIVATE = 'private'
    PUBLIC = 'public'

    type = models.CharField(max_length=255, default=PUBLIC, blank=True)
    name = models.CharField(max_length=255, unique=True, blank=True)

    def get_user_collections(self):
        return UserCollection.objects.all().filter(collection__id=self.id)

    def get_requests(self):
        return Request.objects.all().filter(collection__id=self.id)

    def get_scenarios(self):
        Scenario.objects.all().filter(collection_id=self.id)

    def __str__(self):
        return str(self.id) + ') ' + self.name

    class Meta:
        db_table = 'collections'


class UserCollection(models.Model):
    OWNER = 'owner'
    EDITOR = 'editor'
    VISITOR = 'visitor'

    role = models.CharField(max_length=255, default=VISITOR)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_collections'
        unique_together = ('user', 'collection',)
