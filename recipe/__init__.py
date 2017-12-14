# #app/__init__.py

# from flask_api import FlaskAPI
# from flask_sqlalchemy import SQLAlchemy
# from flask_httpauth import HTTPBasicAuth
# from flask_restful import Resource, Api
# from app.views import AddUser

# # local import
# from instance.config import app_config

# # initialize sql-alchemy
# #auth = HTTPBasicAuth()
# db = SQLAlchemy()
# #session = Session()
# #api = Api()

# config_name = 'development'
# def create_app(config_name):
#     app = FlaskAPI(__name__, instance_relative_config=True)
#     app.config.from_object(app_config[config_name])
#     app.config.from_pyfile('config.py')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)
#     api.init_app(app)
#     api.add_resource(AddUser, "/auth/register", endpoint = "add_user")

#     return app

# app = create_app(config_name)
# api = Api(app)
