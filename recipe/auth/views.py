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
from . import autho
from recipe.models import User
#from . import autho
from recipe.helpers import key_is_not_empty, login_required




# app = Flask(__name__)
# app.config.from_object("config.DevelopmentConfig")
# db = SQLAlchemy(app)
# api = Api(app)

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'
#secret_key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'

#autho = Blueprint('auth', __name__)
api = Api(autho)
#api_login = Api(autho_login)


# def login_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({'message': 'token is missing'})
        
#         s = Serializer(secret_key)
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return jsonify({'message': 'token has expired'}) # valid token, but expired
#         except BadSignature:
#             return jsonify({'message': 'Invalid token'}) # invalid token
#         users = data['userid']
#         user = User.query.filter_by(userid = data['userid']).first()
#         return f(*args, **kwargs)
import re
# def isValidEmail(email):
#     if len(email) > 7:
#         r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
#         if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
#             return True
#         return False
#     return False
def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

def is_username_valid(username):
    if re.match("^[A-Za-z_-]*$", username):
        return True
    return False

def is_firstname_valid(firstname):
    if re.match("^[A-Za-z_-]*$", firstname):
        return True
    return False

def is_lastname_valid(lastname):
    if re.match("^[A-Za-z_-]*$", lastname):
        return True
    return False


class AddUser(Resource):
    #@app.route('/user', methods= ['POST'])
    def post(self):  
        parser = reqparse.RequestParser()
        #parser.add_argument('userid', type = int)
        parser.add_argument('username', type = str, required = True, help='username cannot be empty')
        parser.add_argument('email', type = str, help='email not provided', required=True)
        parser.add_argument('password', type = str, required=True, help='password has to be a minimum of 8 characters')
        parser.add_argument('firstname', type = str, required=True, help='firstname cannot have special characters or intergers')
        parser.add_argument('lastname', type = str, required=True, help='lastname cannot have special characters or intergers')
        args = parser.parse_args()
        #userid = args['userid']
        if key_is_not_empty(args):
            return {'error': 'all fields must be filled'}, 422
        username = args['username']
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        lastname = args['lastname']
        if not is_email_address_valid(email):
            return {'message':'invalid email'}, 400
        if not is_username_valid(username):
            return {'message':'invalid username use phiona format'}, 400
        if not is_firstname_valid(firstname):
            return {'message':'invalid input use format Phiona'}, 400
        if not is_lastname_valid(lastname):
            return {'message':'invalid input use format Basemera'}, 400
        person = User.query.filter_by(username = username, email = email).first()
        if person is None:
            new_user = User(username, email, password, firstname, lastname)
            new_user.hash_password(password)
            new_user.save_user()
            return {'userid': new_user.userid,'Username': new_user.username,  "email":new_user.email, 'lastname': new_user.lastname}, 201
            #return ({"message": "Success"})
        else:
            return {"message": "User already exists"}, 400
    # return {'message':'invalid credentials'}
        

# class EditUser(Resource):
#     @login_required
#     def put(self, userid):
#         parser = reqparse.RequestParser()
#         parser.add_argument('username', type = str)
#         args = parser.parse_args()
#         username = args['username']
#         user = User.query.filter_by(userid = userid).first()
#         if user is None:
#             return ({'message':'user doesnot exist'})
#         user.username = username
#         db.session.commit()
#         return ({'username':user.username})

#     @login_required
#     def delete(self, userid):
#         user = User.query.filter_by(userid = userid).first()
#         if user is None:
#             return ({'message':'user doesnot exist'})
#         username = user.username
#         db.session.delete(user)
#         db.session.commit()
#         return ({'User deleted':username})

class Login(Resource):
    #@login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type = str)
        parser.add_argument('password', type = str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        
        # auth = request.authorization
        # if not auth:
        #     return make_response("login info not provided")
        
        users = User.query.filter_by(username = username).first()
        if not users:
            response = {'message':'user doesnot exist'}
            return make_response(jsonify(response), 401)
            #return make_response("user doesnot exist")
        user = User.verify_password(username, password)
        if user:
            token = g.user.generate_auth_token()
            user =g.user
            response = {'message':'You have successfully logged in', 'token': token.decode('ascii') }
            return make_response(jsonify(response), 200)
        responses = {'message':'invalid credentials'}
        return make_response(jsonify(responses), 401)
        #return make_response("invalid credentials")


api.add_resource(AddUser, '/user') # , endpoint = "add_user"
api.add_resource(Login, '/login')
#api_login.add_resource(Login, '/login')
app.register_blueprint(autho)
#app.register_blueprint(autho_login)
if __name__ == "__main__":
    app.run()

