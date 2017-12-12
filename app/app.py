from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from instance.config import app_config


#from models import db
db = SQLAlchemy()
api = Api()
#app config

config_name = 'development'
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    api.init_app(app)
    
    return app



app = create_app('development')
api = Api(app)
