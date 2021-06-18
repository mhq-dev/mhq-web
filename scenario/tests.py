import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from authentication.models import User
from collection.models import Collection, UserCollection
from request.models import Request, KeyValueContainer
from module.models import Module
from edge.models import Edge
from scenario.models import Scenario


class RequestViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user")
        self.token = Token.objects.create(user=self.user)
        self.generate_basic_database()

    def generate_basic_database(self):
        self.col1 = Collection.objects.create(name='col1', type='private')
        self.req1 = Request.objects.create(collection=self.col1,
                                           name='req1',
                                           http_method=Request.GET,
                                           url='https://60c1f3514f7e880017dc0e65.mockapi.io/scenario')

        self.req2 = Request.objects.create(collection=self.col1,
                                           name='req2',
                                           http_method=Request.GET,
                                           url='https://60c1f3514f7e880017dc0e65.mockapi.io/scenario')

        self.scenario1 = Scenario.objects.create(name='scenario1', collection=self.col1, schedule=None,
                                                 starter_module=None)

        self.module1 = Module.objects.create(scenario=self.scenario1, request=self.req1, x_position=0, y_position=1)
        self.module2 = Module.objects.create(scenario=self.scenario1, request=self.req2, x_position=11, y_position=0)

        Edge.objects.create(source=self.module1, dist=self.module2)

        self.scenario1.starter_module = self.module1
        self.scenario1.save()

    def test_execute_scenario(self):
        response = self.client.get(reverse('scenario-execute', kwargs={'pk': self.scenario1.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # self.client.force_login(self.user)
        # UserCollection.objects.create(user=self.user, collection=self.col1, role='owner')
        # response = self.client.get(reverse('scenario-execute', kwargs={'pk': self.scenario1.id}))
        # print(response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
