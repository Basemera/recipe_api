import re
from functools import wraps
from flask import request, jsonify, make_response, url_for
from .models import User, Blacklist, Serializer, SignatureExpired, BadSignature, secret_key
from api_recipe.models import User, RecipeCategory, Recipes

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
            response = {'message':'token is missing'}, 401
            return make_response(response)
        
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            response = {'message':'token has expired'}, 401
            return make_response(response)
        except BadSignature:
            response = {'message':'Invalid token'}, 401
            return make_response(response)
        users = data['userid']
        user = User.query.filter_by(userid = data['userid']).first()
        return f(*args, **kwargs)
    return decorated

def paginate_categories(page, q, userid):
    if q:
        pagination =  RecipeCategory.query.filter(RecipeCategory.category_name.ilike('%' + q + '%')).filter_by(
                user=userid).paginate(page=page, per_page=8, error_out=False)
    else:
        pagination = RecipeCategory.query.filter_by(user=userid).paginate(page=page, per_page=8, error_out=False)
    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('category.search', q=q, page=page - 1, _external=True)
        else:
            previous = url_for('category.addcategory', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('category.search', q=q, page=page + 1, _external=True)
        else:
            nex = url_for('category.addcategory', page=page + 1, _external=True)
    items = pagination.items
    return items, nex, pagination, previous


def response_with_pagination(previous, nex, count):
    
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count
    })), 200
    
def paginate_recipes(page, q, userid, category):
    if q:
        pagination =  Recipes.query.filter(Recipes.recipe_name.ilike('%' + q + '%')).filter_by(user=userid, category=category).paginate(page=page, per_page=8, error_out=False)
    else:
        pagination = Recipes.query.filter_by(user=userid, category=category).paginate(page=page, per_page=4, error_out=False)
    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('recipe.search', q=q, page=page - 1, category=category,  _external=True)
        else:
            previous = url_for('recipe.getrecipes', page=page - 1, category=category, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('recipe.search', q=q, page=page + 1, category=category, _external=True)
        else:
            nex = url_for('recipe.getrecipes', page=page + 1, category=category,  _external=True)
    items = pagination.items
    return items, nex, pagination, previous