from rest_framework.permissions import BasePermission
from collection.models import UserCollection, Collection
from django.shortcuts import get_object_or_404
from .models import ScenarioHistory


class ScenarioPermission(BasePermission):
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

    def has_object_permission(self, request, view, obj):
        if view.action == 'update' or view.action == 'destroy':
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj.collection)
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True


class ScenarioHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            collection = get_object_or_404(Collection, id=view.kwargs.get('collection_id'))
            if collection.type == Collection.PRIVATE:
                get_object_or_404(UserCollection, user=request.user, collection=collection)
            return True

        if request.method == 'DELETE':
            collection = get_object_or_404(ScenarioHistory, id=view.kwargs.get('pk')).scenario.collection
            user_collection = get_object_or_404(UserCollection, user=request.user, collection=collection)
            if user_collection.role == UserCollection.VISITOR:
                return False
        return True
