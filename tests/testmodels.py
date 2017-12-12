#tests/testmodels
import unittest
import json
from flask import jsonify, json
from app.models import User
from app.app import create_app, db
from werkzeug.datastructures import Headers


class TestUsermodelTestCase(unittest.TestCase):
    """Class representing the Usermodel Test Case"""
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona', 'firstname':'Phiona', 'lastname':'Bas'}
        # def create_apps(self):
        #     """Setup app and its configs"""

        #     config_name = 'testing'

        #     app = create_app(config_name)

        #     return app
        with self.app.app_context():
            db.create_all()
    def test_user_registration(self):
            
            
        data = dict(username='seconduser',
                        firstname='Second',
                        lastname='User',
                        email='bb@c.com',
                        password='87654321'
                        )

        payload = json.dumps(data)

        h = Headers()
        h.add('Content-Type', 'application/json')

        response = self.client().post('/user', headers=h, data=payload)

        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        """teardown all initialized variables."""
        
        # drop all tables
        db.session.remove()
        db.drop_all()
    

        

if __name__ == "__main__":
    unittest.main()
    #self.assertEqual(res.status_code, 200, 'user not created')