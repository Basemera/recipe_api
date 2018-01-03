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
#     """Class representing the Usermodel Test Case"""
#     def test_username_and_email_already_exist(self):
#         data = {'username':'seconduser',
#                 'email':'bb@c.com',
#                 'password':'87654321',
#                 'firstname':'Second',
#                 'lastname':'User'
#         }
#         data1 = {'username':'seconduser',
#                 'email':'nht@c.com',
#                 'password':'87654321',
#                 'firstname':'stela',
#                 'lastname':'kiwa'
#         }
#         with self.client:
#               self.client.post('/user', data=data)
#               response = self.client.post('/user', data=data1)
#               self.assertEqual(response.status_code, 470)


        def test_user_registration(self):
                
                data = {'username':'seconduser',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'Second',
                        'lastname':'User'
                }
                data1 = {'username':'',
                        'email':'bab@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'lastname':'bas'
                }
                data2 = {'username':'',
                        'email':'',
                        'password':'87654321',
                        'firstname':'    ',
                        'lastname':'bas'
                }

                
                #print('data: {}'.format(data))
                payload = json.dumps(data)
                #print(payload)
                h = Headers()
                h.add('Content-Type', 'application/json')
                

                # response = self.client().post("/user", headers=h, data=payload)
                response = self.client.post('/user', data=data)
                response1 = self.client.post('/user', data=data1)
                response2 = self.client.post('/user', data=data2)

                # print("here here")
                # print('response')
                # print(response)
                # print('response')
                # # res = json.loads(response.data)
                # # print(res)
                self.assertEqual(response.status_code, 201)
                self.assertIn('bb@c.com', data['email'])
                self.assertIn('User', data['lastname'])
                self.assertEqual(response1.status_code, 422)
                self.assertEqual(response2.status_code, 422)

        def test_username_is_empty_string(self):
                data1 = {'username':'',
                        'email':'bab@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'lastname':'bas'
                }

                payload = json.dumps(data1)
                #print(payload)
                h = Headers()
                h.add('Content-Type', 'application/json')
                response1 = self.client.post('/user', data=data1)
                result = json.loads(response1.data)
                self.assertEqual(response1.status_code, 422)
                self.assertEqual(result['error'], 'all fields must be filled')

        def test_email_is_empty_string(self):
                data1 = {'username':'phiona',
                        'email':'',
                        'password':'87654321',
                        'firstname':'phiona',
                        'lastname':'bas'
                }

                payload = json.dumps(data1)
                #print(payload)
                h = Headers()
                h.add('Content-Type', 'application/json')
                response1 = self.client.post('/user', data=data1)
                result = json.loads(response1.data)
                self.assertEqual(response1.status_code, 422)
                self.assertEqual(result['error'], 'all fields must be filled')

        def test_password_is_empty_string(self):
                data1 = {'username':'phiona',
                        'email':'basp@tre.com',
                        'password':'',
                        'firstname':'phiona',
                        'lastname':'bas'
                }

                payload = json.dumps(data1)
                #print(payload)
                h = Headers()
                h.add('Content-Type', 'application/json')
                response1 = self.client.post('/user', data=data1)
                result = json.loads(response1.data)
                self.assertEqual(response1.status_code, 422)
                self.assertEqual(result['error'], 'all fields must be filled')

        def test_firstname_is_empty_string(self):
                data1 = {'username':'phiona',
                        'email':'basp@tre.com',
                        'password':'123456789',
                        'firstname':'',
                        'lastname':'bas'
                }

                payload = json.dumps(data1)
                #print(payload)
                h = Headers()
                h.add('Content-Type', 'application/json')
                response1 = self.client.post('/user', data=data1)
                result = json.loads(response1.data)
                self.assertEqual(response1.status_code, 422)
                self.assertEqual(result['error'], 'all fields must be filled')

        def test_lastname_is_empty_string(self):
                data1 = {'username':'phiona',
                        'email':'basp@tre.com',
                        'password':'123456789',
                        'firstname':'phiona',
                        'lastname':''
                }

                payload = json.dumps(data1)
                #print(payload)
                h = Headers()
                h.add('Content-Type', 'application/json')
                response1 = self.client.post('/user', data=data1)
                result = json.loads(response1.data)
                self.assertEqual(response1.status_code, 422)
                self.assertEqual(result['error'], 'all fields must be filled')
        def test_user_already_exists(self):
                payload = json.dumps(self.user)
                #print(payload)
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
                        'lastname':'User'
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
                        'lastname':'User'
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
                        'lastname':'User'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'invalid input on firstname use format Phiona')

        def test_firstname_not_provided(self):
                data = {'username':'phiona',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'lastname':'User'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], {'firstname': 'firstname must be a string'})

        def test_lastname_not_valid(self):
                data = {'username':'phiona',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'lastname':'1234'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'invalid input on lastname use format Basemera')

        def test_lastname_not_provided(self):
                data = {'username':'phiona',
                        'email':'bb@c.com',
                        'password':'87654321',
                        'firstname':'phiona'
                        
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], {'lastname': 'lastname must be a string'})


        def test_email_not_valid(self):
                data = {'username':'phiona',
                        'email':'bb@@c.com',
                        'password':'87654321',
                        'firstname':'phiona',
                        'lastname':'basem'
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
                        'email':'basp@yaho.com'
                }
                response = self.client.post('/user', data=data)
                results = json.loads(response.data)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(results['message'], 'password has to be more than 8 characters')

           
                


    
if __name__ == "__main__":
    unittest.main()
    #self.assertEqual(res.status_code, 200, 'user not created')