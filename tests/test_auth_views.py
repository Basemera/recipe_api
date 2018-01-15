import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from api_recipe import db
from api_recipe.models import User
from api_recipe.auth.views import AddUser, api
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase



class TestUsermodelTestCase(BaseTestCase):
    """Testcase to test the User registration funcionalities"""
    def test_user_registration(self):
        h = Headers()
        h.add('Content-Type', 'application/json')
        response = self.client.post('/register', data=self.user)
        result= json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('bap@gmail.com', str(result))
        
    def test_username_is_empty_string(self):
        data1 = {'username':'',
                'email':'bab@c.com',
                'password':'87654321',
                'firstname':'phiona',
                'confirm_password':'87654321'
        }
        payload = json.dumps(data1)
        h = Headers()
        h.add('Content-Type', 'application/json')
        response1 = self.client.post('/register', data=data1)
        result = json.loads(response1.data)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(result['error'], 'all fields must be filled')
    def test_email_is_empty_string(self):
        data1 = {'username':'phiona',
                'email':'',
                'password':'87654321',
                'firstname':'phiona',
                'confirm_password':'87654321'
        }
        payload = json.dumps(data1)
        h = Headers()
        h.add('Content-Type', 'application/json')
        response1 = self.client.post('/register', data=data1)
        result = json.loads(response1.data)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(result['error'], 'all fields must be filled')
    def test_password_is_empty_string(self):
        data1 = {'username':'phiona',
                'email':'basp@tre.com',
                'password':'',
                'firstname':'phiona',
                'confirm_password':'87654321'
        }
        payload = json.dumps(data1)
        h = Headers()
        h.add('Content-Type', 'application/json')
        response1 = self.client.post('/register', data=data1)
        result = json.loads(response1.data)
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(result['error'], 'all fields must be filled')
    def test_firstname_is_empty_string(self):
            data1 = {'username':'phiona',
                    'email':'basp@tre.com',
                    'password':'123456789',
                    'firstname':'',
                    'confirm_password':'87654321'
            }
            payload = json.dumps(data1)
            h = Headers()
            h.add('Content-Type', 'application/json')
            response1 = self.client.post('/register', data=data1)
            result = json.loads(response1.data)
            self.assertEqual(response1.status_code, 400)
            self.assertEqual(result['error'], 'all fields must be filled')
    def test_confirm_password_is_empty(self):
            data1 = {'username':'phiona',
                    'email':'basp@tre.com',
                    'password':'123456789',
                    'firstname':'phiona',
                    'confirm_password':''
            }
            payload = json.dumps(data1)
            h = Headers()
            h.add('Content-Type', 'application/json')
            response1 = self.client.post('/register', data=data1)
            result = json.loads(response1.data)
            self.assertEqual(response1.status_code, 400)
            self.assertEqual(result['confirm_password'], 
                                    'passwords do not match')
    def test_user_already_exists(self):
            payload = json.dumps(self.user)
            h = Headers()
            h.add('Content-Type', 'application/json')  
            user = self.client.post('/register', data=self.user)
            response = self.client.post('/register', data=self.user)
            results=json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['error'],'User already exists')
    def test_username_not_valid(self):
            data = {'username':1234,
                    'email':'bb@c.com',
                    'password':'87654321',
                    'firstname':'Second',
                    'confirm_password':'87654321'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['username'], 
                            'invalid username cannot begin with numbers')
    def test_username_not_provided(self):
            data = {
                    'email':'bb@c.com',
                    'password':'87654321',
                    'firstname':'Second',
                    'confirm_password':'87654321'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['message'], 
                            {'username': 'username cannot be empty'})
    def test_firstname_not_valid(self):
            data = {'username':'phiona',
                    'email':'bb@c.com',
                    'password':'87654321',
                    'firstname':'1234',
                    'confirm_password':'87654321'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['firstname'], 
                            'invalid firstname cannot have numbers')

    def test_firstname_not_provided(self):
            data = {'username':'phiona',
                    'email':'bb@c.com',
                    'password':'87654321',
                    'confirm_password':'87654321'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['message'], 
                            {'firstname': 'firstname must be a string'})
    def test_passwords_do_not_match(self):
            data = {'username':'phiona',
                    'email':'bb@c.com',
                    'password':'87654321',
                    'firstname':'phiona',
                    'confirm_password':'car'
                    
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['confirm_password'], 
                            'passwords do not match')
    def test_email_not_valid(self):
            data = {'username':'phiona',
                    'email':'bb@@c.com',
                    'password':'87654321',
                    'firstname':'phiona',
                    'confirm_password':'87654321'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['email'], 'invalid email')

    def test_email_not_provided(self):
            data = {'username':'phiona',
                    'password':'87654321',
                    'firstname':'phiona',
                    'lastname':'basem'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['message'], 
                            {'email': 'email not provided'})
    def test_password_not_provided(self):
            data = {'username':'phiona',
                    'firstname':'phiona',
                    'lastname':'basem',
                    'email':'basp@yaho.com'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['message'], 
                            {'password': 'password cannot be empty'})
    def test_password_less_than_9_characters(self):
            data = {'username':'phiona',
                    'firstname':'phiona',
                    'lastname':'basem',
                    'password':'car',
                    'email':'basp@yaho.com',
                    'confirm_password':'car'
            }
            response = self.client.post('/register', data=data)
            results = json.loads(response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(results['password'], 
                            'password must be more than 8 characters')
class TestUserAuthenticationTestCase(BaseTestCase):
    def test_user_login(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 200)
            self.assertEqual(result['message'], 'You have successfully logged in')
            self.assertTrue(result['token'])

    def test_incorrect_credentials(self):
        with self.client:
            data = {'username':'Bas', 'password':'phiona19876650e4'}
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=data)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'invalid credentials')

    def test_nonexistent_user(self):
        data2 = {'username':"Basph", "password":"phiona"}
        with self.client:
            response = self.client.post('/register', data=self.user)
            self.assertEqual(response.status_code, 201)
            responses = self.client.post('/login', data=data2)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'user doesnot exist')

    def test_log_out(self):
        with self.client:
            register_user = self.client.post('/register', data=self.user)
            log_in = self.client.post('/login', data=self.data2)
            results = json.loads(log_in.data.decode())
            auth = results['token']
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/logout', headers=h)
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'logged out')
