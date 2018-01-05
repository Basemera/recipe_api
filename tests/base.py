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
        self.user = {'username': 'Bas', 'email': 'bap@gmail.com', 'password':'phiona2017', 'firstname':'Phiona', 'confirm_password':'phiona2017'}
        self.category = {'category_name':'fish'}
        self.recipe = {'recipe_name':"stew", 'description':"prepared with water"}
        self.data2 ={'username':"Bas", "password":"phiona2017"}
    
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """teardown all initialized variables."""

        with app.app_context():
            db.session.remove()
            db.drop_all()

