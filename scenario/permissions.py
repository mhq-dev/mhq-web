from rest_framework.permissions import BasePermission
from collection.models import UserCollection, Collection
from django.shortcuts import get_object_or_404
from .models import ScenarioHistory


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
