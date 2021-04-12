from rest_framework import permissions

from collection.models import UserCollection, Collection


class RequestPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj.collection)
            if obj.collection.type == Collection.PRIVATE and len(user_collection) != 1:
                return False
        else:
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj.collection)
            if len(user_collection) != 1 or user_collection.role == UserCollection.VISITOR:
                return False

        return True

    def has_permission(self, request, view):
        if request.method == 'POST':
            user_collection = UserCollection.objects.filter(user=request.user,
                                                            collection__id=request.data['collection'])
            if len(user_collection) != 1 or user_collection.role == UserCollection.VISITOR:
                return False

        return True
