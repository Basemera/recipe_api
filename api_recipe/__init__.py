import os
from flask import Flask
from flask_cors import CORS
from flask_api import FlaskAPI
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config

db = SQLAlchemy()
api = Api()

config_name = os.environ.get('APP_SETTINGS')
# def create_app(config_name):
app = FlaskAPI(__name__, instance_relative_config=True)
# app = Flask(__name__)
CORS(app)
app.config.from_object(app_config[config_name])
# app.config.from_pyfile('config.py')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api.init_app(app)
db.init_app(app)

from .auth import autho
from .categories import category
from .recipes import recipe

app.register_blueprint(autho)
app.register_blueprint(category)
app.register_blueprint(recipe)
