from rest_framework.permissions import BasePermission
from collection.models import UserCollection

from scenario.models import Scenario


class ModulePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action == 'update' or view.action == 'destroy':
            user_collection = UserCollection.objects.filter(user=request.user, collection=obj.scenario.collection)
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True

    def has_permission(self, request, view):
        if view.action == 'update' or view.action == 'destroy' or view.action == 'create':
            if not request.user.is_authenticated:
                return False

        if view.action == 'create':
            # TODO find better idea for this
            if 'scenario' not in request.data:
                return False

            scenario = Scenario.objects.filter(id=request.data['scenario'])
            if len(scenario) == 0:
                return False

            user_collection = UserCollection.objects.filter(user=request.user, collection=scenario[0].collection)
            if len(user_collection) == 0 or user_collection[0].role == UserCollection.VISITOR:
                return False

        return True
