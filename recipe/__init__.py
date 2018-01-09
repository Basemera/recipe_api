import os
from flask import Flask
from flask_api import FlaskAPI
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from .auth import autho
from .categories import category
from .recipes import recipe
# from .auth.views import AddUser
# app = Flask(__name__)
# app.config.from_object("recipe.config.DevelopmentConfig")
# db = SQLAlchemy(app)
db = SQLAlchemy()
api = Api()

# config_name = 'development'
def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.init_app(app)
    app.register_blueprint(autho)
    app.register_blueprint(category)
    app.register_blueprint(recipe)
    # api.add_resource(AddUser, "/auth/register", endpoint = "add_user")

    return app

# if __name__ == "__main__":
#     app.run()
