from flask_testing import TestCase
from recipe import app




class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('recipe.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        self.assertTrue(app.config['SECRET_KEY'] == key)
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres@localhost:5432/recipe_api'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('recipe.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        self.assertTrue(app.config['SECRET_KEY'] == key)
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'postgresql://postgres@localhost:5432/test_db'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('recipe.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
        self.assertTrue(app.config['SECRET_KEY'] == key)
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
