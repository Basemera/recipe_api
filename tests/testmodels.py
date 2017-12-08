#tests/testmodels
import unittest
import json
from app.models import User
from app.app import create_app, db

class UsermodelTestCase(unittest.TestCase):
    """Class representing the Usermodel Test Case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
            # create all tables
        db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        
        # drop all tables
        db.session.remove()
        db.drop_all()
    def test_usermodel(self):
        
        #user = {"username": 'Bas', "email": 'bap@gmail.com', "password":'phiona', "firstname":'Phiona', "lastname":'Bas'}
        user = User('Bas', 'bap@gmail.com', 'phiona', 'Phiona', 'Bas')
        res = self.client().post('/auth/register', data = user)
        self. assertEqual(user['username'], 'Bas')

if __name__ == "__main__":
    unittest.main()
    #self.assertEqual(res.status_code, 200, 'user not created')