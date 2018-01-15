import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from itsdangerous import BadSignature, SignatureExpired
from api_recipe import db
from api_recipe.models import User
from api_recipe.auth.views import AddUser, api
from api_recipe.categories.views import Addcategory, api_category
from werkzeug.datastructures import Headers
from base64 import b64encode
from tests.base import BaseTestCase

class TestCategoriesTestCase(BaseTestCase):
    """testing creating categories"""
    def test_creating_categories(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/category', 
                                        headers=h, data=self.category)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(results['message'], 'Category created')

    def test_token_requirred(self):  
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            response = self.client.post('/category', 
                                        headers=h, data=self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(result['message'], 'token is missing')

    def test_token_expired(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            tok1 = "eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxNDU"
            tok2 = "4NjQxNiwiZXhwIjoxNTE0NTkyNDE2fQ."
            tok3 = "eyJ1c2VyaWQiOjE0fQ.5M0O41VxHuzoU0"
            tok4 = "x43XfgS1yAq6XAD441wlUr-UPMmJE"
            auth = tok1+tok2+tok3+tok4
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/category', 
                                        headers=h, data=self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(result['message'], 'token has expired')

    def test_invalid_token(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = 'phiona'
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/category',
                                        headers=h, data=self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(result['message'], 'Invalid token')

    def test_creating_duplicate_category(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/category',
                                        headers=h, data=self.category)
            responses = self.client.post('/category',
                                         headers=h, data=self.category)
            result = json.loads(responses.data)
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'Category already exists')

    def test_empty_string_not_allowed(self):
        data3 = {'category_name':"     "}
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category',
                                                 headers=h, data=data3)
            result = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 422)
            self.assertEqual(result['error'], 'all fields must be filled')


    def test_edit_category(self):
        data3 = {'category_name':"seafood"}
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category',
                                                 headers=h,
                                                 data=self.category)
            category_response = self.client.put('/category/1',
                                                headers=h, data=data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 200)
            self.assertEqual(results['message'], 'category edited')

    def test_edit_nonexistant_category(self):
        data3 = {'category_name':"lunch"}
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category',
                                                 headers=h,
                                                 data=self.category)
            category_response = self.client.put('/category/2',
                                                headers=h, data=data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 404)
            self.assertEqual(results['message'], 'category doesnot exist')

    def test_delete_category(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category',
                                                 headers=h,
                                                 data=self.category)
            category_response = self.client.delete('/category/1', headers=h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 200)
            self.assertEqual(results['message'], 'successfully deleted')

    def test_deleting_nonexistant_category(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.delete('/category/1', headers=h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 404)
            self.assertEqual(results['message'], 'category doesnot exist')

    def test_getting_all_categories(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category',
                                                 headers=h,
                                                 data=self.category)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 201)
            self.assertIn('fish', results['category_name'])
    def test_validate_category_name(self):
        data3 = {'category_name':1234}
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category',
                                                 headers=h, data=data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 400)
            r1 = 'invalid input use'
            r2 = ' format peas'
            r = r1+r2
            self.assertEqual(results['message'], r)
    
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
