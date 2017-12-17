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


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('recipe.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg')
        self.assertTrue(app.config['DEBUG'] is True)
        #self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres:phiona@localhost:5432/recipe_api'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('recipe.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        #self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres:phiona@localhost:5432/test_db'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('recipe.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
