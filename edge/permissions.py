from rest_framework.permissions import BasePermission
from collection.models import UserCollection

from module.models import Module


class EdgePermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'update' or view.action == 'destroy':
            user_collection = UserCollection.objects.filter(
                user=request.user, collection=obj.source.scenario.collection
            )
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True

    def has_permission(self, request, view):
        if view.action == 'update' or view.action == 'destroy' or view.action == 'create':
            if not request.user.is_authenticated:
                return False

        if view.action == 'create':
            # TODO find better idea for this
            if 'source' not in request.data or 'dist' not in request.data:
                return False

            source = Module.objects.filter(id=request.data['source'])
            if len(source) == 0:
                return False

            user_collection = UserCollection.objects.filter(
                user=request.user, collection=source[0].scenario.collection
            )
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True
