from rest_framework import permissions

from collection.models import UserCollection


class CollectionPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'destroy':
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj)
            if len(user_collection) == 0 or user_collection[0].role != UserCollection.OWNER:
                return False

        if view.action == 'update':
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj)
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True

    def has_permission(self, request, view):
        if view.action == 'update' or view.action == 'destroy' or view.action == 'create':
            if not request.user.is_authenticated:
                return False

        return True


def has_add_user_permission(applicant_user_collection):
    if applicant_user_collection.role != UserCollection.OWNER:
        return False
    return True


def has_remove_or_promote_user_permission(applicant_user_collection, requested_user_collection):
    if applicant_user_collection.role != UserCollection.OWNER:
        return False
    if requested_user_collection.role == UserCollection.OWNER:
        return False
    return True
