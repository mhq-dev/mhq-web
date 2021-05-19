from rest_framework.permissions import BasePermission, SAFE_METHODS
from collection.models import UserCollection
from django.shortcuts import get_object_or_404

from module.models import Module
from .models import Edge
from scenario.models import Scenario


class EdgePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(UserCollection, user=request.user, collection=obj.source.scenario.collection)
        if user.role == UserCollection.VISITOR:
            return False
        return True

    def has_permission(self, request, view):
        if request.method == 'POST':
            module_source = get_object_or_404(Module, id=request.data['source'])
            collection_id = module_source.scenario.collection
            user_collection = get_object_or_404(UserCollection, user=request.user,
                                                collection=collection_id)
            if user_collection.role == UserCollection.VISITOR:
                return False
        if request.method == 'GET':
            collection = get_object_or_404(Edge, id=view.kwargs['id']).source.scenario.collection
            if collection.type == 'public':
                return True
            user_collection = get_object_or_404(UserCollection, user=request.user,
                                                collection=collection)
            if user_collection.role == UserCollection.VISITOR:
                return False
        return True
