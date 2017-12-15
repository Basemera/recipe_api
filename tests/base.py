from flask_testing import TestCase
import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, api, db


class BaseTestCase(unittest.TestCase):
    """Class representing the Usermodel Test Case"""
    def setUp(self):
        app.config.from_object("recipe.config.TestingConfig")
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

