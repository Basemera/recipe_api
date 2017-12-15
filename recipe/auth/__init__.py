from flask import Blueprint



"""Creating Blueprints for the login and user"""

autho = Blueprint('auth', __name__, url_prefix='/auth/register')

#from . import views