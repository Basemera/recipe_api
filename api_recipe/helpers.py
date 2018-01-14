import re
from functools import wraps
from flask import request, jsonify
from .models import User, Blacklist, Serializer, SignatureExpired, BadSignature, secret_key

def values_is_empty(args):
    """function to make sure empty spaces cannot be passed in arguments"""
    keys = ('username', 'email', 'password', 'firstname')
    for key in keys:
        if value_is_space(args[key]) == '':
            return True

def value_is_empty(args):
    """function to make sure empty spaces cannot be passed in arguments"""
    key = ('category_name')
    if value_is_space(args[key]) == '':
        return True
    return False

def valuess_is_empty(args):
    """function to make sure empty spaces cannot be passed in arguments"""
    keyss = ('recipe_name', 'description')
    for key in keyss:
        if value_is_space(args[key]) == '':
            return True

def value_is_space(string):
    """function to make sure empty spaces cannot be passed in arguments"""
    return string.strip()

def is_category_name_valid(category_name):
    """method to validate the category name [a-zA-Z-\s]"""
    if re.match("^[A-Za-z_\s-]*$", category_name):
        return True
    return False

def login_required(f):
    """a function to allow access to protected resources"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """a function to allow access to protected resources"""
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            valid_token = Blacklist.query.filter_by(blacklist_token=token).first()
            if valid_token:
                return ({'message':"you are logged out"})

        if not token:
            return jsonify({'message': 'token is missing'})
        
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return jsonify({'message': 'token has expired'})
        except BadSignature:
            return jsonify({'message': 'Invalid token'})
        users = data['userid']
        user = User.query.filter_by(userid = data['userid']).first()
        return f(*args, **kwargs)
    return decorated
