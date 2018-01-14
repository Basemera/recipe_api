import re
from flask import request, jsonify, g, make_response
from sqlalchemy import exc
from flask_restful import reqparse, Resource, Api
from flask_httpauth import HTTPBasicAuth
from api_recipe import create_app
from api_recipe.helpers import values_is_empty, login_required
from api_recipe.models import User, Blacklist, secret_key, auth
from . import autho

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
        """This handles post requests for this view
        ---
        Tags:
          - User Authentication
        Parameters:
          - in: Body
            name: Body
            required: True
            type: String
            description: This registers a new user
        responses:
          201:
            description: User created
        """
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
        returned = {}
        if not is_email_address_valid(email):
            returned['email']= 'invalid email'
        if not is_username_valid(username):
            returned['username']= 'invalid username cannot begin with numbers'
        if not is_firstname_valid(firstname):
            returned['firstname']= 'invalid firstname cannot have numbers'
        if confirm_password != password:
            returned['confirm_password']= 'passwords do not match'
        if len(password) < 8:
            returned['password']= 'password must be more than 8 characters'
        if returned:
            return returned, 400
        person = User.query.filter_by(username=username, email=email).first()
        if person is None: 
            new_user = User(username, email, password, firstname)
            new_user.hash_password(password)
            try:
                new_user.save_user()
                return {
                    'userid': new_user.userid, 'Username': new_user.username,
                    "email": new_user.email, 'firstname':new_user.firstname}, 201
            except exc.IntegrityError:
                return ({"error":'username already exists please choose another one'})
        else:
            return {"error": "User already exists"}, 400

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

class Logout(Resource):
    """A resource that allow users to log out"""
    @login_required
    def post(self):
        """A function to allow users to log out"""
        authorisation = request.headers.get('x-access-token')
        userid = User.verify_auth_token(authorisation)
        if not authorisation:
            return ({"message":"You are not logged in"}), 400
        blacklist=Blacklist(userid, auth)
        blacklist.save_token()
        return ({'message':'logged out'}), 200


api.add_resource(AddUser, '/register')  # , endpoint = "add_user"
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')