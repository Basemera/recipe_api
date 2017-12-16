from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
#from app.app import app, db
#from flask_restful import Api
from flask_restful import reqparse, Resource, Api, marshal_with
#from app import app
#from app.app import app
#from app.models import User
from flask import abort, g, jsonify, Blueprint
#       from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
#from app.marsh import *
#rom marshmallow import pprint
from functools import wraps
from recipe import app, db
from recipe.models import User
#from . import autho
from recipe.helpers import key_is_not_empty




# app = Flask(__name__)
# app.config.from_object("config.DevelopmentConfig")
# db = SQLAlchemy(app)
# api = Api(app)

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'
#secret_key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'

autho = Blueprint('auth', __name__)
api = Api(autho)


class AddUser(Resource):
    #@app.route('/user', methods= ['POST'])
    def post(self):  
        parser = reqparse.RequestParser()
        #parser.add_argument('userid', type = int)
        parser.add_argument('username', type = str, required = True)
        parser.add_argument('email', type = str)
        parser.add_argument('password', type = str)
        parser.add_argument('firstname', type = str)
        parser.add_argument('lastname', type = str)
        args = parser.parse_args()
        #userid = args['userid']
        if key_is_not_empty(args):
            return {'error': 'all fields must be filled'}, 400
        username = args['username'].strip()
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        lastname = args['lastname']
        person = User.query.filter_by(username = username, email = email).first()
        if person is None:
            new_user = User(username, email, password, firstname, lastname)
            #new_user.hash_password(password)
            new_user.save_user()
            return {'userid': new_user.userid,'Username': new_user.username,  "email":new_user.email, 'lastname': new_user.lastname}, 201
            #return ({"message": "Success"})
        else:
            return {"message": "User already exists"}



api.add_resource(AddUser, '/user/') # , endpoint = "add_user"
app.register_blueprint(autho)
if __name__ == "__main__":
    app.run()

