from flask_sqlalchemy import SQLAlchemy
from app.app import db
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

    @staticmethod
    def get_all_users():
        return User.query.all()
    #method to hasg the password using passlib
    def hash_password(self, password):
        self.password = password
        self.password = pwd_context.encrypt(password)

    def verify_passwords(self, password):
        return pwd_context.verify(password, self.password)

    
    def generate_auth_token(self, expiration = 6000):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({ 'userid': self.userid })

    @auth.verify_password
    def verify_password(username_or_token, password):
    # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if user:
            #user = session.query(User).filter_by(userid = userid).one()
            g.user = user
            return True
            
        else:
        # try to authenticate with username/password
            user = session.query(User).filter_by(username = username_or_token).first()
            if not user or not user.verify_passwords(password):
                return False
            g.user = user
            return True
        

    #method to verify a tioken
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = data['userid']
        # user = User.query.get(data['userid'])
        return user
