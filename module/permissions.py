from rest_framework.permissions import BasePermission
from collection.models import UserCollection
from django.shortcuts import get_object_or_404

from module.models import Module
from scenario.models import Scenario


class ModulePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(UserCollection, user=request.user, collection=obj.scenario.collection)
        if user.role == UserCollection.VISITOR:
            return False
        return True

    def has_permission(self, request, view):
        if request.method == 'POST':
            collection_id = get_object_or_404(Scenario, id=request.data['scenario']).collection
            user_collection = get_object_or_404(UserCollection, user=request.user,
                                                collection=collection_id)
            if user_collection.role == UserCollection.VISITOR:
                return False
        if request.method == 'GET':
            collection = get_object_or_404(Module, id=view.kwargs['module_id']).scenario.collection
            if collection.type == 'public':
                return True
            user_collection = get_object_or_404(UserCollection, user=request.user,
                                                collection=collection)
            if user_collection.role == UserCollection.VISITOR:
                return False
        return True
