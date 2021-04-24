from rest_framework.permissions import BasePermission
from collection.models import UserCollection, Collection


class ScenarioPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            user_collection = UserCollection.objects.all().filter(user=request.user,
                                                                  collection_id=request.data['collection'])
            if len(user_collection) < 1 or user_collection.first().role == UserCollection.VISITOR:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        user_collection = UserCollection.objects.filter(user=request.user, collection=obj.collection)
        if request.method == 'GET':
            if obj.collection.type == Collection.PRIVATE and len(user_collection) != 1:
                return False
        else:
            if len(user_collection) != 1 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True
