import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, db
from recipe.models import User
#from app.app import app, db
from recipe.auth.views import AddUser, api
from recipe.categories.views import Addcategory, api_category
#from app.views import AddUser
from werkzeug.datastructures import Headers
from base64 import b64encode
from tests.base import BaseTestCase

# sample = BaseTestCase()
# h = sample.user_blah()

class TestCategoriesTestCase(BaseTestCase):
    """testing creating categories"""
    def test_creating_categories(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data=self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
        
            response = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result['message'], 'Category created')

    def test_creating_duplicate_category(self):
        data2 = {'username':"Bas", "password":"phiona"}
    
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
        
            response = self.client.post('/category', headers = h, data = self.category)
            responses = self.client.post('/category', headers = h, data = self.category)
            result = json.loads(responses.data)
            # self.assertEqual(response.status_code, 201)
            # self.assertEqual(result['message'], 'Category created')
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'Category already exists')

    def test_empty_string_not_allowed(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':"     "}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
        
            category_response = self.client.post('/category', headers = h, data = data3)
            result = json.loads(category_response.data)
            # self.assertEqual(response.status_code, 201)
            # self.assertEqual(result['message'], 'Category created')
            self.assertEqual(category_response.status_code, 422)
            self.assertEqual(result['error'], 'all fields must be filled')


    def test_edit_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':"seafood"}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.put('/category/1', headers = h, data = data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 200)
            self.assertEqual(results['message'], 'category edited')
            # self.assertEqual(category_response.status_code, 422)
            # self.assertEqual(result['error'], 'all fields must be filled')

    def test_edit_nonexistant_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':"seafood"}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.put('/category/2', headers = h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 404)
            self.assertEqual(results['message'], 'category doesnot exist')

    def test_delete_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #data3 = {'category_name':"seafood"}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.delete('/category/1', headers = h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 200)
            self.assertEqual(results['message'], 'successfully deleted')

    def test_deleting_nonexistant_category(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #data3 = {'category_name':"seafood"}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
            #category_response = self.client.post('/category', headers = h, data = self.category)
            category_response = self.client.delete('/category/1', headers = h)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 404)
            self.assertEqual(results['message'], 'category doesnot exist')

    def test_getting_all_categories(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':"seafood"}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            
            #print (result)
            #self.assertEqual(responses.status_code, 200)
            #self.assertEqual(result['message'], 'You have successfully logged in')
            #self.assertTrue(result['token'])
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = self.category)
            #category_response = self.client.post('/category', headers = h, data = data3)
            results = json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 201)
            self.assertIn('fish', results['category_name'])
    def test_validate_category_name(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'category_name':1234}
        #self.client = app.test_client()
        with self.client:
            response = self.client.post('/user', data = self.user)
            #self.assertEqual(response.status_code, 201)
            #response = self.client.post('/login', data = data1)
            # h = Headers()
            # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
            responses = self.client.post('/login', data = data2)
            #result = jsonify(responses)
            result = json.loads(responses.data.decode())
            auth =result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category_response = self.client.post('/category', headers = h, data = data3)
            results =json.loads(category_response.data)
            self.assertEqual(category_response.status_code, 400)
            self.assertEqual(results['message'],'invalid input use format peas')

    