from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource
#from app import app
from app.app import api, db, app, create_app
from app.models import *
# from app.marsh import *
# from marshmallow import pprint
from functools import wraps

@api.representation("text/csv")
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp

class AddUser(Resource):
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
        #print(username)
        email = args['email']
        password = args['password']
        firstname = args['firstname']
        lastname = args['lastname']
        person = User.query.filter_by(username = username).first()
        email = User.query.filter_by(email = email).first()
        if person is None:
            new_user = User(username, password, email, firstname, lastname)
            new_user.hash_password(password)
            new_user.save_user()
            #return jsonify({'userid': new_user.userid,'Username': args['username'],  "email":args['email'], 'Password': new_user.password})
            return ({"message": "Success"})
        else:
            return ({"message": "User already exists"})

