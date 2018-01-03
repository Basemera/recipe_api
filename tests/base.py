from flask_testing import TestCase
import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, db
from recipe.auth.views import api
from werkzeug.datastructures import Headers

def set_up():
    pass
class BaseTestCase(unittest.TestCase):
    """Class representing the Usermodel Test Case"""
    def setUp(self):
        app.config.from_object("recipe.config.TestingConfig")
        self.client = app.test_client()
        self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona1984', 'firstname':'Phiona', 'lastname':'Bas'}
        self.category = {'category_name':"fish"}
        self.recipe = {'recipe_name':"stew", 'description':"prepared with water"}
        self.data2 ={'username':"Bas", "password":"phiona1984"}
        # def create_apps(self):
        #     """Setup app and its configs"""

        #     config_name = 'testing'
    
    # @staticmethod
    # def user_blah(self):
    #     app.config.from_object("recipe.config.TestingConfig")
    #     self.client = app.test_client()
    #     self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona', 'firstname':'Phiona', 'lastname':'Bas'}
    #     self.category = {'category_name':"fish"}
    #     data2 ={'username':"Bas", "password":"phiona"}
    #     #self.client = app.test_client()
    #     with self.client:
    #         response = self.client.post('/user', data = self.user)
    #         #self.assertEqual(response.status_code, 201)
    #         #response = self.client.post('/login', data = data1)
    #         # h = Headers()
    #         # h.add('Authorization', "Basic%s" %b64encode(b"username:password").decode("ascii"))
    #         responses = self.client.post('/login', data = data2)
    #         #result = jsonify(responses)
    #         result = json.loads(responses.data.decode())
            
    #         #print (result)
    #         #self.assertEqual(responses.status_code, 200)
    #         #self.assertEqual(result['message'], 'You have successfully logged in')
    #         #self.assertTrue(result['token'])
    #         auth = result['token']
    #         #token = User.verify_auth_token(auth)
    #         h = Headers()
    #         h.add('x-access-token', auth)
    #         return h


        #     app = create_app(config_name)

        #     return app
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """teardown all initialized variables."""
        # drop all tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

