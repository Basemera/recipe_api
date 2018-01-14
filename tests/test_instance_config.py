from flask_testing import TestCase
import os
from flask import Flask
from flask_api import FlaskAPI
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from api_recipe.auth import autho
from api_recipe.categories import category
from api_recipe.recipes import recipe
from api_recipe import create_app




class TestDevelopmentConfig(TestCase):


    # config_name = 'testing'
    def create_app(self):
        app = FlaskAPI(__name__, instance_relative_config=True)
        app.config.from_object(app_config['development'])
        app.config.from_pyfile('config.py')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy()
        db.init_app(app)
        api = Api()
        api.init_app(app)
        app.register_blueprint(autho)
        app.register_blueprint(category)
        app.register_blueprint(recipe)
        # api.add_resource(AddUser, "/auth/register", endpoint = "add_user")

        return app

    def setUp(self):
        self.app = create_app('development')

    def test_app_is_development(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        self.assertTrue(self.app.config['SECRET_KEY'] == key)
        self.assertTrue(self.app.config['DEBUG'] == True)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres@localhost:5432/recipe_api'
        )

#
class TestTestingConfig(TestCase):
    # config_name = 'testing'
    def create_app(self):
        app = FlaskAPI(__name__, instance_relative_config=True)
        app.config.from_object(app_config['testing'])
        app.config.from_pyfile('config.py')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy()
        db.init_app(app)
        api = Api()
        api.init_app(app)
        app.register_blueprint(autho)
        app.register_blueprint(category)
        app.register_blueprint(recipe)
        return app
    def setUp(self):
        self.app = create_app('testing')

    def test_app_is_testing(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        print (self.app.config['TESTING'])
        self.assertTrue(self.app.config['SECRET_KEY'] == key)
        self.assertTrue(self.app.config['DEBUG'] == True)
        self.assertTrue(self.app.config['TESTING'] == True)
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres@localhost:5432/test_db'
        )


class TestProductionConfig(TestCase):
    db = SQLAlchemy()
    api = Api()

    # config_name = 'testing'
    def create_app(self):
        app = FlaskAPI(__name__, instance_relative_config=True)
        app.config.from_object(app_config['production'])
        app.config.from_pyfile('config.py')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy()
        db.init_app(app)
        api = Api()
        api.init_app(app)
        app.register_blueprint(autho)
        app.register_blueprint(category)
        app.register_blueprint(recipe)
        return app
    def setUp(self):
        self.app = create_app('production')

    def test_app_is_production(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        self.assertTrue(self.app.config['SECRET_KEY'] == key)
        self.assertFalse(self.app.config['DEBUG'] == True)
        self.assertFalse(self.app.config['TESTING'] == True)

class TestStagingConfig(TestCase):
    db = SQLAlchemy()
    api = Api()

    # config_name = 'testing'
    def create_app(self):
        app = FlaskAPI(__name__, instance_relative_config=True)
        app.config.from_object(app_config['staging'])
        app.config.from_pyfile('config.py')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy()
        db.init_app(app)
        api = Api()
        api.init_app(app)
        app.register_blueprint(autho)
        app.register_blueprint(category)
        app.register_blueprint(recipe)
        return app

    def setUp(self):
        self.app = create_app('staging')

    def test_app_is_staging(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        self.assertTrue(self.app.config['SECRET_KEY'] == key)
        self.assertTrue(self.app.config['DEBUG'] == True)
        self.assertTrue(self.app.config['TESTING'] == False)
