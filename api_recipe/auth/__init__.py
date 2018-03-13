from flask import Blueprint
from flask_restful import Api

from . views import AddUser, Login, Logout, Home

"""Creating Blueprints for the login and user"""

autho = Blueprint('auth', __name__)
api = Api(autho)

api.add_resource(AddUser, '/register')  # , endpoint = "add_user"
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Home, '/')
