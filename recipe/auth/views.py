import re
from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with
from flask import abort, g, jsonify, Blueprint
from flask_httpauth import HTTPBasicAuth
from recipe import app, db
from recipe.helpers import values_is_empty, login_required
from . import autho
from recipe.models import User


auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'

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
        """This method allows for the creation of users"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='username cannot be empty')
        parser.add_argument('email', type=str,
                            help='email not provided', required=True)
        parser.add_argument('password', type=str, required=True,
                            help='password cannot be empty')
        parser.add_argument('firstname', type=str,
                            required=True, help='firstname must be a string')
        parser.add_argument('confirm_password', type=str, required=True,
                            help='cannot be empty')
        args = parser.parse_args()
        if values_is_empty(args):
            return {'error': 'all fields must be filled'}, 400
        username = args['username']
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        confirm_password = args['confirm_password']
        if not is_email_address_valid(email):
            return {'message': 'invalid email'}, 400
        if not is_username_valid(username):
            return {'message': 'invalid username use phiona format'}, 400
        if not is_firstname_valid(firstname):
            return {'message': 'invalid input use format Phiona'}, 400
        # if confirm_password is None:
        #     return {'message': 'all fields required'}, 400
        if len(password) < 8:
            return {'message': 'password should be more than 8 characters'}, 400
        person = User.query.filter_by(username=username, email=email).first()
        if person is None:
            new_user = User(username, email, password, firstname)
            if confirm_password==password:
                new_user.hash_password(password)
                new_user.save_user()
                return {'userid': new_user.userid, 'Username': new_user.username,
                "email": new_user.email, 'firstname':new_user.firstname}, 201
            return ({"message":"passwords do not match"}), 400
        else:
            return {"message": "User already exists"}, 400


class Login(Resource):
    """A resource that will allow users to login"""
    def post(self):
        """A function that will allow a user to log in"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        users = User.query.filter_by(username=username).first()
        if not users:
            response = {'message': 'user doesnot exist'}
            return make_response(jsonify(response), 401)
        user = User.verify_password(username, password)
        if user:
            token = g.user.generate_auth_token()
            user = g.user
            response = {'message': 'You have successfully logged in',
                        'token': token.decode('ascii')}
            return make_response(jsonify(response), 200)
        responses = {'message': 'invalid credentials'}
        return make_response(jsonify(responses), 401)


api.add_resource(AddUser, '/user')  # , endpoint = "add_user"
api.add_resource(Login, '/login')
app.register_blueprint(autho)
# if __name__ == "__main__":
#     app.run()
