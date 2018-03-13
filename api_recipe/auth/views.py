import re
from flask import request, jsonify, g, make_response
from sqlalchemy import exc
from flask_restful import reqparse, Resource, Api
from flask_httpauth import HTTPBasicAuth
from api_recipe.helpers import values_is_empty, login_required
from api_recipe.models import User, Blacklist, secret_key, auth
# from . import autho

# api = Api(autho)
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
        username = request.data['username']
        firstname = request.data['firstname']
        email = request.data['email']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        args = {'username':username, 'firstname':firstname, 'email':email, 'password':password, 'confirm_password':confirm_password}
        if values_is_empty(args):
            return {'error': 'all fields must be filled'}, 400
        username = args['username']
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        confirm_password = args['confirm_password']
        if args['email'] == "":
            return ({'email': 'email not provided'})
        returned = {}
        if not is_email_address_valid(email):
            # returned.append('invalid email')
            returned['email']= 'invalid email'
        if not is_username_valid(username):
            # returned.append('inva/lid username cannot begin with numbers')
            returned['username']= 'inva/lid username cannot begin with numbers'
        if not is_firstname_valid(firstname):
            # returned.append('invalid firstname cannot have numbers')
            returned['firstname']= 'invalid firstname cannot have numbers'
        if confirm_password != password:
            # returned.append('passwords do not match')
            returned['confirm_password']= 'passwords do not match'
        if len(password) < 8:
            # returned.append('password must be more than 8 characters')
            returned['password']= 'password must be more than 8 characters'
        if returned:
            return returned, 400
        person = User.query.filter_by(username=username, email=email).first()
        if person is None: 
            new_user = User(username, email, password, firstname)
            new_user.hash_password(password)
            try:
                new_user.save_user()
                response = {'message': 'Successfully registered'}
                return make_response(jsonify(response), 201) 
                # return {
                #     'userid': new_user.userid, 'Username': new_user.username,
                #     "email": new_user.email, 'firstname':new_user.firstname}, 201
            except exc.IntegrityError:
                return ({"error":'username already exists please choose another one'}), 400
        else:
            return {"error": "User already exists"}, 400

class Login(Resource):
    """A resource that will allow users to login"""
    def post(self):
        """A function that will allow a user to log in"""
        
        username = request.data['username']
        password = request.data['password']
        # args = parser.parse_args()
        args = {'username':username, 'password':password}
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
        blacklist=Blacklist(userid, authorisation)
        blacklist.save_token()
        return ({'message':'logged out'}), 200

class Home(Resource):
    def get(self):
        return ({'message': 'API working'})


# api.add_resource(AddUser, '/register')  # , endpoint = "add_user"
# api.add_resource(Login, '/login')
# api.add_resource(Logout, '/logout')
# api.add_resource(Home, '/')