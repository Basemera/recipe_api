from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
#from app.app import app, db
#from flask_restful import Api
from flask_restful import reqparse, Resource, Api, marshal_with
#from app import app
#from app.app import app
#from app.models import User
from flask import abort, g, jsonify
#       from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
#from app.marsh import *
#rom marshmallow import pprint
from functools import wraps
from recipe_api import app, db, api
from models import User




# app = Flask(__name__)
# app.config.from_object("config.DevelopmentConfig")
# db = SQLAlchemy(app)
# api = Api(app)

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'
#secret_key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'

# class User(db.Model):
#     __tablename__ = 'user'
#     userid = db.Column(db.Integer,  primary_key = True, autoincrement = True)
#     username = db.Column(db.String(100), unique = True, nullable= False, index = True)
#     email = db.Column(db.String(100), unique = True, index = True)
#     password = db.Column(db.String(128), nullable = False)
#     firstname = db.Column(db.String(100), unique = True, nullable= False, index = True)
#     lastname = db.Column(db.String(100), unique = True, nullable= False, index = True)
#     datecreated = db.Column(db.DateTime, default=db.func.current_timestamp())
#     datemodified = db.Column(
#         db.DateTime, default=db.func.current_timestamp(),
#         onupdate=db.func.current_timestamp())
#     #recipecategory = db.relationship('RecipeCategory', backref = 'owner', lazy = 'dynamic')

#     def __init__(self, username, email, password, firstname, lastname):
#         #self.userid = userid
#         self.username = username
#         self.email = email
#         self.password = password
#         self.firstname = firstname
#         self.lastname = lastname


#     #function to add a user to the database
#     def save_user(self):
#         db.session.add(self)
#         db.session.commit()
#     #method to delete a user from the database
#     def delete_user(self):
#         db.session.delete(self)
#         db.session.commit()

#     @staticmethod
#     def get_all_users():
#         return User.query.all()
#     #method to hasg the password using passlib
#     def hash_password(self, password):
#         self.password = password
#         self.password = pwd_context.encrypt(password)

#     def verify_passwords(self, password):
#         return pwd_context.verify(password, self.password)

    
#     def generate_auth_token(self, expiration = 6000):
#         s = Serializer(secret_key, expires_in = expiration)
#         return s.dumps({ 'userid': self.userid })

#     @auth.verify_password
#     def verify_password(username_or_token, password):
#     # first try to authenticate by token
#         user = User.verify_auth_token(username_or_token)
#         if user:
#             #user = session.query(User).filter_by(userid = userid).one()
#             g.user = user
#             return True
            
#         else:
#         # try to authenticate with username/password
#             user = session.query(User).filter_by(username = username_or_token).first()
#             if not user or not user.verify_passwords(password):
#                 return False
#             g.user = user
#             return True
        

#     #method to verify a tioken
#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(secret_key)
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None # valid token, but expired
#         except BadSignature:
#             return None # invalid token
#         user = data['userid']
#         # user = User.query.get(data['userid'])
#         return user


# @api.representation("text/csv")
# def output_json(data, code, headers=None):
#     """Makes a Flask response with a JSON encoded body"""
#     resp = make_response(json.dumps(data), code)
#     resp.headers.extend(headers or {})
#     return resp

class AddUser(Resource):
    #@app.route('/user', methods= ['POST'])
    def post(self):  
        parser = reqparse.RequestParser()
        #parser.add_argument('userid', type = int)
        parser.add_argument('username', type = str)
        parser.add_argument('email', type = str)
        parser.add_argument('password', type = str)
        parser.add_argument('firstname', type = str)
        parser.add_argument('lastname', type = str)
        args = parser.parse_args()
        #userid = args['userid']
        username = args['username']
        print(username)
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
if __name__ == "__main__":
    app.run()

