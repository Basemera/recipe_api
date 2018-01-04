import re
from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with
from flask import abort, g, jsonify, Blueprint
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
from functools import wraps
from recipe import app, db
from recipe.helpers import values_is_empty, login_required
from . import autho
from recipe.models import User


auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'
#secret_key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'

api = Api(autho)


def is_email_address_valid(email):
    """Validate the email."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True


def is_username_valid(username):
    """Validate the username"""
    if re.match("^[A-Za-z_-]*$", username):
        return True
    return False


def is_firstname_valid(firstname):
    """Validate the firstname"""
    if re.match("^[A-Za-z_-]*$", firstname):
        return True
    return False


def is_lastname_valid(lastname):
    """Validate the lastname"""
    if re.match("^[A-Za-z_-]*$", lastname):
        return True
    return False


class AddUser(Resource):
    """This resource allows users to register using a username, email, 
    password, firstname and lastname"""
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='username cannot be empty')
        parser.add_argument('email', type=str,
                            help='email not provided', required=True)
        parser.add_argument('password', type=str, required=True,
                            help='password cannot be empty')
        parser.add_argument('firstname', type=str,
                            required=True, help='firstname must be a string')
        parser.add_argument('lastname', type=str, required=True,
                            help='lastname must be a string')
        args = parser.parse_args()
        if values_is_empty(args):
            return {'error': 'all fields must be filled'}, 400
        username = args['username']
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        lastname = args['lastname']
        if not is_email_address_valid(email):
            return {'message': 'invalid email'}, 400
        if not is_username_valid(username):
            return {'message': 'invalid username use phiona format'}, 400
        if not is_firstname_valid(firstname):
            return {'message': 'invalid input on firstname use format Phiona'}, 400
        if not is_lastname_valid(lastname):
            return {'message': 'invalid input on lastname use format Basemera'}, 400
        if len(password) < 8:
            return {'message': 'password has to be more than 8 characters'}, 400
        person = User.query.filter_by(username=username, email=email).first()
        if person is None:
            new_user = User(username, email, password, firstname, lastname)
            new_user.hash_password(password)
            new_user.save_user()
            return {'userid': new_user.userid, 'Username': new_user.username,
          "email": new_user.email, 'lastname': new_user.lastname}, 201
        else:
            return {"message": "User already exists"}, 400


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

class Login(Resource):
    #@login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        # auth = request.authorization
        # if not auth:
        #     return make_response("login info not provided")

        users = User.query.filter_by(username=username).first()
        if not users:
            response = {'message': 'user doesnot exist'}
            return make_response(jsonify(response), 401)
            # return make_response("user doesnot exist")
        user = User.verify_password(username, password)
        if user:
            token = g.user.generate_auth_token()
            user = g.user
            response = {'message': 'You have successfully logged in',
                        'token': token.decode('ascii')}
            return make_response(jsonify(response), 200)
        responses = {'message': 'invalid credentials'}
        return make_response(jsonify(responses), 401)
        # return make_response("invalid credentials")


api.add_resource(AddUser, '/user')  # , endpoint = "add_user"
api.add_resource(Login, '/login')
#api_login.add_resource(Login, '/login')
app.register_blueprint(autho)
# app.register_blueprint(autho_login)
if __name__ == "__main__":
    app.run()
