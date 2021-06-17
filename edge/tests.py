import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from authentication.models import User
from collection.models import Collection, UserCollection
from condition.models import Condition
from edge.managers import EdgeManager
from edge.models import Edge, Statement
from module.models import Module
from request.models import Request
from scenario.models import Scenario


class EdgeViewSetTestCase(APITestCase):

    def setUp(self):
        self.generate_basic_database()
        self.token = Token.objects.create(user=self.user)

    def generate_basic_database(self):
        self.user = User.objects.create_user(username="amirh")
        self.collection = Collection.objects.create(type='public', name='edge_test')
        self.user_collection = UserCollection.objects.create(
            role='owner',
            user=self.user,
            collection=self.collection
        )
        self.req = Request.objects.create(
            collection=self.collection,
            name='edge_test_request',
            http_method=Request.GET,
            url='https://6094a286f082a4001736b248.mockapi.io/api/furit'
        )
        self.scenario = Scenario.objects.create(
            name='edge_test_scenario',
            collection=self.collection
        )
        self.node1 = Module.objects.create(scenario=self.scenario, request=self.req)
        self.node2 = Module.objects.create(scenario=self.scenario, request=self.req)
        self.node3 = Module.objects.create(scenario=self.scenario, request=self.req)
        self.node4 = Module.objects.create(scenario=self.scenario, request=self.req)
        self.edge1 = Edge.objects.create(source=self.node1, dist=self.node2)
        self.statement1 = Statement.objects.create(edge=self.edge1)
        self.condition1 = Condition.objects.create(
            statement=self.statement1,
            first='hi',
            second='hi'
        )

    def test_edge_create(self):
        response = self.client.post(reverse('edge-create'), json.dumps({
            'source': self.node1.id,
            'dist': self.node3.id,
            'statements': []
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('edge-create'), json.dumps({
            'source': self.node1.id,
            'dist': self.node3.id,
            'statements': []
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('edge-create'), json.dumps({
            'source': self.node1.id,
            'dist': self.node2.id,
            'statements': []
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('edge-create'), json.dumps({
            'dist': self.node3.id,
            'statements': []
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('edge-create'), json.dumps({
            'source': self.node1.id,
            'dist': self.node4.id,
            'statements': [
                {
                    'conditions': [
                        {
                            'first': 'hi',
                            'second': 'hi'
                        },
                        {
                            'operator': 'exist',
                            'first': 'hi',
                            'second': 'bye'
                        }
                    ]
                },
                {
                    'conditions': [
                        {
                            'first_toke': 'num',
                            'first': '12',
                            'second_token': 'timestamp',
                            'second': '2021-06-17T20:48:50.451419+04:30'
                        }
                    ]
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()['statements']), 2)
        self.assertEqual(len(response.json()['statements'][0]['conditions']), 2)
        self.assertEqual(len(response.json()['statements'][1]['conditions']), 1)
        response = self.client.post(reverse('edge-create'), json.dumps({
            'source': self.node1.id,
            'dist': self.node4.id,
            'statements': [
                {
                    'conditions': [
                        {
                            'first': 'hi',
                            'second': 'hi'
                        },
                        {
                            'operator': 'exist',
                            'first': 'hi',
                            'second': 'bye'
                        }
                    ]
                },
                {
                    'conditions': [
                        {
                            'first_toke': 'num',
                            'first': '12',
                            'second_token': 'timestamp',
                            'second': '2021-06-17T20:48:50.451419+04:30'
                        }
                    ]
                }
            ]
        }), content_type='application/json')

    def test_edge_detail(self):
        response = self.client.get(reverse('edge_detail', kwargs={'pk': self.edge1.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('edge_detail', kwargs={'pk': self.edge1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['statements']), 1)
        self.assertEqual(len(response.json()['statements'][0]['conditions']), 1)
        response = self.client.put(reverse('edge_detail', kwargs={'pk': self.edge1.id}), json.dumps({
            'statements': [
                {
                    'conditions': [
                        {
                            'first': 'hi',
                            'second': 'hi'
                        },
                        {
                            'operator': 'exist',
                            'first': 'hi',
                            'second': 'bye'
                        }
                    ]
                },
                {
                    'conditions': [
                        {
                            'first_toke': 'num',
                            'first': '12',
                            'second_token': 'timestamp',
                            'second': '2021-06-17T20:48:50.451419+04:30'
                        }
                    ]
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['statements']), 2)
        self.assertEqual(len(response.json()['statements'][0]['conditions']), 2)
        self.assertEqual(len(response.json()['statements'][1]['conditions']), 1)
        response = self.client.put(reverse('edge_detail', kwargs={'pk': self.edge1.id}), json.dumps({
            'statements': [
                {
                    'conditions':[]
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['statements']), 1)
        self.assertEqual(len(response.json()['statements'][0]['conditions']), 0)
        response = self.client.delete(reverse('edge_detail', kwargs={'pk': self.edge1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EdgeManagerTestCase(APITestCase):

    def setUp(self):
        self.generate_basic_database()
        self.token = Token.objects.create(user=self.user)

    def generate_basic_database(self):
        self.user = User.objects.create_user(username="sadra")
        self.collection = Collection.objects.create(type='public', name='edge_manager_test')
        self.user_collection = UserCollection.objects.create(
            role='owner',
            user=self.user,
            collection=self.collection
        )
        self.req = Request.objects.create(
            collection=self.collection,
            name='edge_manager_test_request',
            http_method=Request.GET,
            url='https://6094a286f082a4001736b248.mockapi.io/api/furit'
        )
        self.scenario = Scenario.objects.create(
            name='edge_manager_test_scenario',
            collection=self.collection
        )
        self.node1 = Module.objects.create(scenario=self.scenario, request=self.req)
        self.node2 = Module.objects.create(scenario=self.scenario, request=self.req)
        self.edge1 = Edge.objects.create(source=self.node1, dist=self.node2)
        self.statement1 = Statement.objects.create(edge=self.edge1)
        self.condition1 = Condition.objects.create(statement=self.statement1, first='hi', second='hi')
        self.condition2 = Condition.objects.create(statement=self.statement1, first='hi', second='hi')
        self.statement2 = Statement.objects.create(edge=self.edge1)
        self.condition3 = Condition.objects.create(statement=self.statement2, first='hi', second='hi')
        self.condition4 = Condition.objects.create(statement=self.statement2, first='hi', second='hi')

    def test_edge_manager(self):
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.condition1.first = 'bye'
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.condition3.first = 'bye'
        self.condition3.save()
        self.assertEqual(EdgeManager(self.edge1).check(), False)
        self.condition1.operator = 'start_with'
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), False)
        self.condition1.second = 'by'
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.condition1.operator = 'contains'
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.condition1.first = 'yyyyybbbb'
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), False)
        self.condition1.first_token = 'num'
        self.condition1.first = 12
        self.condition1.second_token = 'num'
        self.condition1.second = 12
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.condition1.first = 13
        self.condition1.save()
        self.assertEqual(EdgeManager(self.edge1).check(), False)
        self.condition1.delete()
        self.condition2.delete()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.statement2.delete()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
        self.statement1.delete()
        self.assertEqual(EdgeManager(self.edge1).check(), True)
