import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, db
from recipe.models import User
from recipe.auth.views import AddUser, api
from recipe.categories.views import Addcategory, api_category
from werkzeug.datastructures import Headers
from base64 import b64encode
from tests.base import BaseTestCase

class TestCategoriesTestCase(BaseTestCase):
    """testing creating categories"""
    def test_creating_categories(self):
        
        with self.client:
            response = self.client.post('/user', data=self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
        
            response = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result['message'], 'Category created')

    def test_token_requirred(self):
        
        with self.client:
            response = self.client.post('/user', data=self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
        
            response = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'token is missing')

    def test_token_expired(self):
        
        with self.client:
            response = self.client.post('/user', data=self.user)
            
            responses = self.client.post('/login', data = self.data2)
            
            result = json.loads(responses.data.decode())
            auth = 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxNDU4NjQxNiwiZXhwIjoxNTE0NTkyNDE2fQ.eyJ1c2VyaWQiOjE0fQ.5M0O41VxHuzoU0x43XfgS1yAq6XAD441wlUr-UPMmJE'
            
            h = Headers()
            h.add('x-access-token', auth)
        
            response = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'token has expired')

    def test_invalid_token(self):
        
        with self.client:
            response = self.client.post('/user', data=self.user)
            
            responses = self.client.post('/login', data = self.data2)
            
            result = json.loads(responses.data.decode())
            auth = 'phiona'
            
            h = Headers()
            h.add('x-access-token', auth)
        
            response = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'Invalid token')

    def test_creating_duplicate_category(self):

        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
        
            response = self.client.post('/category', headers = h, data = self.category)
            responses = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(responses.data)
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'Category already exists')

    def test_empty_string_not_allowed(self):
        
        data3 = {'category_name':"     "}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
        
            category_response = self.client.post('/category', headers = h, data = data3)
            result = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 422)
            self.assertEqual(result['error'], 'all fields must be filled')


    def test_edit_category(self):
       
        data3 = {'category_name':"seafood"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.put('/category/1', headers = h, data = data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 200)
            self.assertEqual(results['message'], 'category edited')

    def test_edit_nonexistant_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':"lunch"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.put('/category/2', headers = h, data = data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 404)
            self.assertEqual(results['message'], 'category doesnot exist')

    def test_delete_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
    
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.delete('/category/1', headers = h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 200)
            self.assertEqual(results['message'], 'successfully deleted')

    def test_deleting_nonexistant_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.delete('/category/1', headers = h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 404)
            self.assertEqual(results['message'], 'category doesnot exist')

    def test_getting_all_categories(self):
        data3 = {'category_name':"seafood"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 201)
            self.assertIn('fish', results['category_name'])
    def test_validate_category_name(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':1234}
        with self.client:
            response = self.client.post('/user', data = self.user)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            auth =result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = data3)
            results =json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 400)
            self.assertEqual(results['message'],'invalid input use format peas')

    