import os
#from app.app import api, db, app
#from app.views import AddUser, api
#from app.app import create_app
#from instance.config import app_config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask import Flask
from flask_restful import Api
#from views import AddUser
#from flask_httpauth import HTTPBasicAuth
#from instance.config import app_config


#from models import db


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app)
api = Api(app)

    # app.config.from_pyfile('config.py')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.app = app
    # db.init_app(app)
    # api.init_app(app)
    
    #return app



#app = create_app(config_name)
# api = Api(app)
# db.init_app(app)
#api.add_resource(AddUser, '/user/') # , endpoint = "add_user"
if __name__ == "__main__":
    app.run()
