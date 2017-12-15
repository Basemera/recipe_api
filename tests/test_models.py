#tests/testmodels
import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, api, db
from recipe.models import User
#from app.app import app, db
from recipe.auth.views import AddUser
#from app.views import AddUser
from werkzeug.datastructures import Headers
from .base import BaseTestCase


class TestUsermodelTestCase(BaseTestCase):
    """Class representing the Usermodel Test Case"""
    # def setUp(self):
    #     app.config.from_object("recipe.config.TestingConfig")
    #     self.client = app.test_client()
    #     self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona', 'firstname':'Phiona', 'lastname':'Bas'}
    #     # def create_apps(self):
    #     #     """Setup app and its configs"""

    #     #     config_name = 'testing'

    #     #     app = create_app(config_name)

    #     #     return app
    #     with app.app_context():
    #         db.create_all()
    
    # def tearDown(self):
    #     """teardown all initialized variables."""
    #     # drop all tables
    #     with app.app_context():
    #         db.session.remove()
    #         db.drop_all()

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
        
        #print('data: {}'.format(data))
        payload = json.dumps(data)
        #print(payload)
        h = Headers()
        h.add('Content-Type', 'application/json')
        

        # response = self.client().post("/user", headers=h, data=payload)
        response = self.client.post('/auth/register/user/', data=data)
        response1 = self.client.post('/auth/register/user/', data=data1)
        # print("here here")
        # print('response')
        # print(response)
        # print('response')
        # # res = json.loads(response.data)
        # # print(res)
        self.assertEqual(response.status_code, 201)
        self.assertIn('bb@c.com', data['email'])
        self.assertIn('User', data['lastname'])
        self.assertEqual(response1.status_code, 404)


    
if __name__ == "__main__":
    unittest.main()
    #self.assertEqual(res.status_code, 200, 'user not created')