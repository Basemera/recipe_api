#tests/testmodels
import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, db
from recipe.models import User
#from app.app import app, db
from recipe.auth.views import AddUser, api
#from app.views import AddUser
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase


class TestUsermodelTestCase(BaseTestCase):
        """Testcase to test the User registration funcionalities"""
        def test_user_registration(self):
                
                data = {'username':'seconduser',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'Second',
                        'confirm_password':'87654321'
                }
                data1 = {'username':'',
                        'email':'bab@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'confirm_password':'87654321'
                }
                data2 = {'username':'',
                        'email':'',
                        'password':'87654321',
                        'firstname':'    ',
                        'confirm_password':'87654321'
                }
                payload = json.dumps(data)
                h = Headers()
                h.add('Content-Type', 'application/json')
        
                response = self.client.post('/user', data=data)

                self.assertEqual(response.status_code, 201)
                self.assertIn('bb@c.com', data['email'])

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
                response1 = self.client.post('/user', data=data1)
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
                response1 = self.client.post('/user', data=data1)
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
                response1 = self.client.post('/user', data=data1)
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
                response1 = self.client.post('/user', data=data1)
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
                response1 = self.client.post('/user', data=data1)
                result = json.loads(response1.data)
                self.assertEqual(response1.status_code, 400)
                self.assertEqual(result['message'], 'passwords do not match')
        def test_user_already_exists(self):
                payload = json.dumps(self.user)
                h = Headers()
                h.add('Content-Type', 'application/json')  
                user = self.client.post('/user', data=self.user)
                response = self.client.post('/user', data=self.user)
                results=json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'],'User already exists')

                

        def test_username_not_valid(self):
                data = {'username':1234,
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'Second',
                        'confirm_password':'87654321'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'invalid username use phiona format')

        def test_username_not_provided(self):
                data = {
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'Second',
                        'confirm_password':'87654321'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], {'username': 'username cannot be empty'})

        def test_firstname_not_valid(self):
                data = {'username':'phiona',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'1234',
                        'confirm_password':'87654321'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'invalid input use format Phiona')

        def test_firstname_not_provided(self):
                data = {'username':'phiona',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'confirm_password':'87654321'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], {'firstname': 'firstname must be a string'})


        def test_passwords_do_not_match(self):
                data = {'username':'phiona',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'confirm_password':'car'
                        
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'passwords do not match')


        def test_email_not_valid(self):
                data = {'username':'phiona',
                        'email':'bb@@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'confirm_password':'basem'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'invalid email')

        def test_email_not_provided(self):
                data = {'username':'phiona',
                        'password':'87654321',
                        'firstname':'phiona',
                        'lastname':'basem'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], {'email': 'email not provided'})

        def test_password_not_provided(self):
                data = {'username':'phiona',
                        'firstname':'phiona',
                        'lastname':'basem',
                        'email':'basp@yaho.com'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], {'password': 'password cannot be empty'})

        def test_password_not_less_9characters(self):
                data = {'username':'phiona',
                        'firstname':'phiona',
                        'lastname':'basem',
                        'password':'car',
                        'email':'basp@yaho.com',
                        'confirm_password':'car'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'password should be more than 8 characters')

           
                


    
if __name__ == "__main__":
    unittest.main()