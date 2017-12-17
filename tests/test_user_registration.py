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
#               self.client.post('/user/', data=data)
#               response = self.client.post('/user/', data=data1)
#               self.assertEqual(response.status_code, 400)


    def test_user_registration_with_validation(self):
        
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



    
if __name__ == "__main__":
    unittest.main()
    #self.assertEqual(res.status_code, 200, 'user not created')