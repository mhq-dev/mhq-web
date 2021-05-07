from rest_framework import permissions

from collection.models import UserCollection


class RequestPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'update' or view.action == 'destroy':
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj.collection)
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True

    def has_permission(self, request, view):
        if view.action == 'update' or view.action == 'destroy' or view.action == 'create':
            if not request.user.is_authenticated:
                return False

        if view.action == 'create':
            # TODO find better idea for this
            if 'collection' not in request.data:
                return False

            user_collection = UserCollection.objects.filter(user=request.user,
                                                            collection__id=request.data['collection'])
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True
