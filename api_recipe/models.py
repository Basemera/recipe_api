from flask_sqlalchemy import SQLAlchemy
from . import db
from flask import abort, g, jsonify
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth(scheme='Token')
secret_key = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'





class User(db.Model):
    """User model This class represents the user model"""
    __tablename__ = 'users'
    userid = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True,
                         nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(100), nullable=False, index=True)
    #lastname = db.Column(db.String(100), nullable=False, index=True)
    datecreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    datemodified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    recipe_category = db.relationship(
        'RecipeCategory', backref='owner', lazy='dynamic')
    recipes = db.relationship('Recipes', backref='owner', lazy='dynamic')

    def __init__(self, username, email, password, firstname):
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        #self.lastname = lastname

    
    def save_user(self):
        """function to add a user to the database"""
        db.session.add(self)
        db.session.commit()
    

    def delete_user(self):
        """function to delete a user from the database"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        """function to get all users from the database"""
        return User.query.all()

    def hash_password(self, password):
        """function to hash the password"""
        self.password = password
        self.password = pwd_context.encrypt(password)

    def verify_passwords(self, password):
        """function to verify that provided password is the same as the 
        hashed password"""
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600000):
        """function to generate the authentication token"""
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'userid': self.userid})

    @staticmethod
    def verify_auth_token(token):
        """function to verify that the token is valid ie not expired or 
        invalid"""
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = data['userid']
        return user

    @auth.verify_password
    def verify_password(username_or_token, password):
        """function to verify the provided token or password"""
        user = User.verify_auth_token(username_or_token)
        if user:
            g.user = user
            return True

        else:
            user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_passwords(password):
                return False
            g.user = user
            return True

    


class RecipeCategory(db.Model):
    """RecipeCategory model This class represents the recipe category 
    model"""
    __tablename__ = 'recipe_category'
    category_id = db.Column(db.Integer,  primary_key=True, 
     autoincrement=True)
    category_name = db.Column(db.String(200), index=True)
    datecreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    datemodified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    user = db.Column(db.Integer, db.ForeignKey(User.userid, ondelete="CASCADE"))
    recipes = db.relationship('Recipes', backref='categories', 
    lazy='dynamic')
    
    def __init__(self, category_name, user):
        """initialise the class"""
        self.user = user
        self.category_name = category_name

    def save_category(self):
        """method to save a category to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_category(self):
        """method to delete a user from the database"""
        db.session.delete(self)
        db.session.commit()

    def get_paginate(q, page):
        """ Method to get all categories using pagination """
        CATEGORIES = RecipeCategory.query.paginate(page, 4, False)
        return CATEGORIES

    @staticmethod
    def get_all_categories():
        """ Method to get all categories."""
        return RecipeCategory.query.all()

    def __repr__(self):
        return "<Category %r>" % (self.category_name)


class Recipes(db.Model):
    """Recipes model This class represents the recipe category model"""
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_name = db.Column('name', db.String(250), nullable=False, index=True)
    description = db.Column('description', db.String(
        250), nullable=False, index=True)
    datecreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    datemodified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    user = db.Column('userid', db.Integer, db.ForeignKey(User.userid, ondelete="CASCADE"))
    category = db.Column('category_id', db.Integer,
                         db.ForeignKey(RecipeCategory.category_id, ondelete="CASCADE"))

    def __init__(self, recipe_name, description, user, category):
        """initialise the class"""
        self.user = user
        self.recipe_name = recipe_name
        self.category = category
        self.description = description

    def __repr__(self):
        return "<Recipe %r>" % (self.recipe_name)

    def save_recipe(self):
        """method to save a recipe to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_recipe(self):
        """method to delete a recipe from the database"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_recipes():
        """method to get all recipes from the database"""
        return Recipes.query.all()

class Blacklist(db.Model):
    """Blacklist model This class represents the blacklist model"""
    __tablename__ = 'blacklist'
    number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datecreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    userid = db.Column('userid', db.Integer, nullable=False, index=True)
    blacklist_token = db.Column('blacklist', db.String, nullable=False, index=True, unique=True)

    def __init__(self, userid, blacklist_token):
        """initialise the class"""
        self.userid = userid
        self.blacklist_token = blacklist_token

    def __repr__(self):
        return "<Recipe %r>" % (self.name)

    def save_token(self):
        """method to save a token to the blacklist table"""
        db.session.add(self)
        db.session.commit()

    def delete_recipe(self):
        """method to delete a token from the blacklist table"""
        db.session.delete(self)
        db.session.commit()
