from flask import Flask, render_template, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource
from app import app
from app.app import db, app, api, session
from app.models import *
from app.marsh import *
from marshmallow import pprint
from functools import wraps
from . import autho_login

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'phiona'






class Login(Resource):
    #@login_required
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('username', type = str)
        # parser.add_argument('password', type = str)
        # args = parser.parse_args()
        # username = args['username']
        # password = args['password']
        
        auth = request.authorization
        if not auth:
            return make_response("login info not provided")
        
        users = User.query.filter_by(username = auth.username).first()
        if not users:
            return make_response("user doesnot exist")
        user = User.verify_password(auth.username, auth.password)
        if user:
            token = g.user.generate_auth_token()
            user =g.user
            return jsonify({ 'token': token.decode('ascii') })
        return make_response("invalid credentials")