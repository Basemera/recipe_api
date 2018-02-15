import os
from flask import Flask
from flask_cors import CORS
from flask_api import FlaskAPI
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from .auth import autho
from .categories import category
from .recipes import recipe

db = SQLAlchemy()
api = Api()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.init_app(app)
    app.register_blueprint(autho)
    app.register_blueprint(category)
    app.register_blueprint(recipe)
    return app
