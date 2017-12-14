#tests/testmodels
import unittest
import json
from flask import jsonify, json
from recipe_api import app, db, api
from models import User
#from app.app import app, db
from views import AddUser
#from app.views import AddUser
from werkzeug.datastructures import Headers


class TestUsermodelTestCase(unittest.TestCase):
    """Class representing the Usermodel Test Case"""
    def setUp(self):
        app.config.from_object("config.TestingConfig")
        self.client = app.test_client()
        self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona', 'firstname':'Phiona', 'lastname':'Bas'}
        # def create_apps(self):
        #     """Setup app and its configs"""

        #     config_name = 'testing'

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

    def test_user_registration(self):
        
        data = {'username':'seconduser',
                'email':'bb@c.com',
                'password':'87654321',
                'firstname':'Second',
                'lastname':'User'
        }
        
        #print('data: {}'.format(data))
        payload = json.dumps(data)
        #print(payload)
        h = Headers()
        h.add('Content-Type', 'application/json')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] =="postgresql://postgres:phiona@localhost:5432/test_db")

        # response = self.client().post("/user", headers=h, data=payload)
        response = self.client.post('/user/', data=data)
        
        # print("here here")
        # print('response')
        # print(response)
        # print('response')
        # # res = json.loads(response.data)
        # # print(res)
        self.assertEqual(response.status_code, 201)
        self.assertIn('bb@c.com', data['email'])
        self.assertIn('User', data['lastname'])

    
if __name__ == "__main__":
    unittest.main()
    #self.assertEqual(res.status_code, 200, 'user not created')