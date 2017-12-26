from functools import wraps
from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with
from .models import *
def key_is_not_empty(args):
    keys = ('username', 'email', 'password', 'firstname', 'lastname')
    #keyss = ('category_name')
    for key in keys:
        if key_is_space(args[key]) == '':
            return True
    # for key in keyss:
    #     if key_is_space(args[key]) == '':
    #         return True
def keys_is_not_empty(args):
    key = ('category_name')
    #keyss = ('category_name')
    
    if key_is_space(args[key]) == '':
        return True

def keyss_is_not_empty(args):
    keyss = ('recipe_name', 'description')
    for key in keyss:
    
        if key_is_space(args[key]) == '':
            return True

def key_is_space(string):
    return string.strip()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'token is missing'})
        
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return jsonify({'message': 'token has expired'}) # valid token, but expired
        except BadSignature:
            return jsonify({'message': 'Invalid token'}) # invalid token
        users = data['userid']
        user = User.query.filter_by(userid = data['userid']).first()
        print(user)
        return f(*args, **kwargs)
    return decorated

# resource_fields = {'category_name':fields.String, 'category_id':fields.String}



