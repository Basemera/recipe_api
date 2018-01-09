import unittest
from recipe import  db, create_app


class BaseTestCase(unittest.TestCase):
    """Class representing the Usermodel Test Case"""
    def setUp(self):
        self.app = create_app('testing')
        self.app.config.from_object("instance.config.TestingConfig")
        self.client = self.app.test_client()
        self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona2017', 'firstname':'Phiona', 'confirm_password':'phiona2017'}
        self.category = {'category_name':'fish'}
        self.recipe = {'recipe_name':"stew", 'description':"prepared with water"}
        self.data2 ={'username':"Bas", "password":"phiona2017"}
    
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """teardown all initialized variables."""

        with self.app.app_context():
            db.session.remove()
            db.drop_all()

