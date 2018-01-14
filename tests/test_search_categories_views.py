import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from api_recipe import db, create_app
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase
from api_recipe.recipes.views import *
from api_recipe.auth.views import AddUser, api
from api_recipe.categories.views import Addcategory, api_category

class TestSearchTestCase(BaseTestCase):
    def test_search_categories(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get(
                '/category/search?q=fish&per_page=2&page=1',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)         
    def test_search_none_existing_category(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get(
                                '/category/search?q=peas&per_page=2&page=1',
                                     headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 404)
            self.assertEqual(result['message'], 'search item not found')           
    def test_search_no_search_parameter_provided(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get('/category/search', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(result['message'], 'search item not provided')

    def test_page_parameter_not_provided(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get('/category/search?q=&per_page=2&page=',
                                    headers=h)
            results = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(results['message'], 'search item not provided')
    def test_page_parameter_provided_is_string(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get(
                                '/category/search?q=fish&per_page=2&page=k',
                                    headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_per_page_parameter_not_provided(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get(
                                '/category/search?q=fish&per_page=&page=1',
                                     headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_page_parameter_provided_is_string(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get(
                                '/category/search?q=fish&per_page=k&page=1',
                                     headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_get_all_categories_for_a_user(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            search = self.client.get('/category', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
