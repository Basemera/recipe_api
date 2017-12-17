from flask import Blueprint



"""Creating Blueprints for the login and user"""

autho = Blueprint('auth', __name__)
autho_login = Blueprint('login', __name__)

#from . import views