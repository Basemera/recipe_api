from flask_sqlalchemy import SQLAlchemy
from app.app import create_app, db, session
#from app.app import api, app, db, session
from flask import abort, g, jsonify
#       from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'


#create the User model
class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer,  primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), unique = True, nullable= False, index = True)
    email = db.Column(db.String(100), unique = True, index = True)
    password = db.Column(db.String(128), nullable = False)
    firstname = db.Column(db.String(100), unique = True, nullable= False, index = True)
    lastname = db.Column(db.String(100), unique = True, nullable= False, index = True)
    datecreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    datemodified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    #recipecategory = db.relationship('RecipeCategory', backref = 'owner', lazy = 'dynamic')

    def __init__(self, username, email, password, firstname, lastname):
        #self.userid = userid
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname


    #function to add a user to the database
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    #method to delete a user from the database
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()