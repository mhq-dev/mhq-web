import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authentication.models import User
from collection.models import Collection, UserCollection
from request.models import Request, KeyValueContainer


class RequestViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="amirh")
        self.token = Token.objects.create(user=self.user)
        self.generate_basic_database()

    def generate_basic_database(self):
        self.col1 = Collection.objects.create(type='private', name='col1')
        UserCollection.objects.create(user=self.user, collection=self.col1, role=UserCollection.OWNER)
        self.req1 = Request.objects.create(collection=self.col1, name='req1', http_method=Request.GET, url='req1.com')
        KeyValueContainer.objects.create(request=self.req1, type=KeyValueContainer.HEADER, key='kvc1', value='kvc1-val')
        KeyValueContainer.objects.create(request=self.req1, type=KeyValueContainer.PARAM, key='kvc2', value='kvc2-val')
        KeyValueContainer.objects.create(request=self.req1, type=KeyValueContainer.PARAM, key='kvc3', value='kvc3-val')
        self.col2 = Collection.objects.create(type='private', name='col2')
        UserCollection.objects.create(user=self.user, collection=self.col2, role=UserCollection.EDITOR)
        self.req2 = Request.objects.create(collection=self.col2, name='req2', http_method=Request.GET, url='req2.com')
        KeyValueContainer.objects.create(request=self.req2, type=KeyValueContainer.HEADER, key='kvc1', value='kvc1-val')
        KeyValueContainer.objects.create(request=self.req2, type=KeyValueContainer.PARAM, key='kvc2', value='kvc2-val')
        KeyValueContainer.objects.create(request=self.req2, type=KeyValueContainer.PARAM, key='kvc3', value='kvc3-val')
        self.col3 = Collection.objects.create(type='private', name='col3')
        UserCollection.objects.create(user=self.user, collection=self.col3, role=UserCollection.VISITOR)
        self.req3 = Request.objects.create(collection=self.col3, name='req3', http_method=Request.GET, url='req3.com')
        KeyValueContainer.objects.create(request=self.req3, type=KeyValueContainer.HEADER, key='kvc1', value='kvc1-val')
        KeyValueContainer.objects.create(request=self.req3, type=KeyValueContainer.PARAM, key='kvc2', value='kvc2-val')
        KeyValueContainer.objects.create(request=self.req3, type=KeyValueContainer.PARAM, key='kvc3', value='kvc3-val')
        self.col4 = Collection.objects.create(type='public', name='col4')
        self.req4 = Request.objects.create(collection=self.col4, name='req4', http_method=Request.GET, url='req4.com')
        KeyValueContainer.objects.create(request=self.req4, type=KeyValueContainer.HEADER, key='kvc1', value='kvc1-val')
        KeyValueContainer.objects.create(request=self.req4, type=KeyValueContainer.PARAM, key='kvc2', value='kvc2-val')
        KeyValueContainer.objects.create(request=self.req4, type=KeyValueContainer.PARAM, key='kvc3', value='kvc3-val')
        self.col5 = Collection.objects.create(type='private', name='col5')
        self.req5 = Request.objects.create(collection=self.col5, name='req5', http_method=Request.GET, url='req5.com')
        KeyValueContainer.objects.create(request=self.req5, type=KeyValueContainer.HEADER, key='kvc1', value='kvc1-val')
        KeyValueContainer.objects.create(request=self.req5, type=KeyValueContainer.PARAM, key='kvc2', value='kvc2-val')
        KeyValueContainer.objects.create(request=self.req5, type=KeyValueContainer.PARAM, key='kvc3', value='kvc3-val')
        self.req6 = Request.objects.create(collection=self.col1,
                                           name='get-collection-list-req',
                                           http_method=Request.GET,
                                           url='https://6094a286f082a4001736b248.mockapi.io/api/furit')

    def test_request_list(self):
        response = self.client.get(reverse('request-list', kwargs={'collection_id': self.col1.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse('request-list', kwargs={'collection_id': self.col4.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('request-list', kwargs={'collection_id': self.col1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('request-list', kwargs={'collection_id': self.col3.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('request-list', kwargs={'collection_id': self.col5.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_create(self):
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col1.id,
                                                "name": "unauthorized-req",
                                                "http_method": Request.GET,
                                                "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({'collection': self.col4.id,
                                                'name': 'unauthorized-req',
                                                'http_method': Request.GET,
                                                'url': 'uar.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col1.id,
                                                "name": "created-req1",
                                                "http_method": Request.GET,
                                                "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col2.id,
                                                "name": "created-req2",
                                                "http_method": Request.GET,
                                                "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col3.id,
                                                "name": "permission-denied-req",
                                                "http_method": Request.GET,
                                                "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({'collection': self.col4.id,
                                                'name': 'permission-denied-req',
                                                'http_method': Request.GET,
                                                'url': 'uar.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"name": "without-col-id-req",
                                                "http_method": Request.GET,
                                                "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col1.id,
                                                "name": "with-wrong-method-req",
                                                "http_method": 'chert',
                                                "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col1.id,
                                                "name": "with-header-req",
                                                "http_method": Request.GET,
                                                "url": "uar.com",
                                                "headers": [
                                                    {"enable": True,
                                                     "key": "key1",
                                                     "value": "val1"}
                                                ]}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Request.objects.get(name='with-header-req').get_headers()), 1)
        response = self.client.post(reverse('request-create'),
                                    json.dumps({"collection": self.col1.id,
                                                "name": "with-params-req",
                                                "http_method": Request.GET,
                                                "url": "uar.com",
                                                "params": [
                                                    {"enable": False,
                                                     "key": "key1",
                                                     "value": "val1"}
                                                ]}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Request.objects.get(name='with-params-req').get_params()), 1)

    def test_request_detail(self):
        response = self.client.get(reverse('request-detail', kwargs={'pk': self.req1.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse('request-detail', kwargs={'pk': self.req4.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('request-detail', kwargs={'pk': self.req1.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(reverse('request-detail', kwargs={'pk': self.req4.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('request-detail', kwargs={'pk': self.req1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('request-detail', kwargs={'pk': self.req3.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('request-detail', kwargs={'pk': self.req5.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('request-detail', kwargs={'pk': self.req1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('request-detail', kwargs={'pk': self.req2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(reverse('request-detail', kwargs={'pk': self.req3.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(reverse('request-detail', kwargs={'pk': self.req5.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_update(self):
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req1.id}),
                                   json.dumps({"name": "unauthorized-req",
                                               "http_method": Request.GET,
                                               "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req4.id}),
                                   json.dumps({'name': 'unauthorized-req',
                                               'http_method': Request.GET,
                                               'url': 'uar.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_login(user=self.user)
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req1.id}),
                                   json.dumps({"name": "updated-req1",
                                               "http_method": Request.GET,
                                               "url": "uar.com"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req2.id}),
                                   json.dumps({'name': 'updated-req2',
                                               'http_method': Request.GET,
                                               'url': 'uar.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req3.id}),
                                   json.dumps({'name': 'updated-req3',
                                               'http_method': Request.GET,
                                               'url': 'uar.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req4.id}),
                                   json.dumps({'name': 'updated-req4',
                                               'http_method': Request.GET,
                                               'url': 'uar.com'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req1.id}),
                                   json.dumps({"name": "updated-headers-req",
                                               "http_method": Request.GET,
                                               "url": "uar.com",
                                               "headers": [
                                                   {"enable": True,
                                                    "key": "key1",
                                                    "value": "val1"},
                                                   {"enable": True,
                                                    "key": "key2",
                                                    "value": "val2"}
                                               ]}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.req1.get_headers()), 2)
        self.assertEqual(len(self.req1.get_params()), 2)
        response = self.client.put(reverse('request-detail', kwargs={'pk': self.req2.id}),
                                   json.dumps({"name": "updated-params-req",
                                               "http_method": Request.GET,
                                               "url": "uar.com",
                                               "params": [
                                                   {"enable": True,
                                                    "key": "key1",
                                                    "value": "val1"}
                                               ]}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.req2.get_params()), 1)
        self.assertEqual(len(self.req2.get_headers()), 1)

    def test_execute_request(self):
        response = self.client.get(reverse('request-execute', kwargs={'pk': self.req6.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('request-execute', kwargs={'pk': self.req6.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.json()['status']), status.HTTP_200_OK)
        self.assertEqual(len(response.json()['body']), 3)
