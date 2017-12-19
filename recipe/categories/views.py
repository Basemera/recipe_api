import requests
import json
from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with, fields
from flask import abort, g, jsonify, Blueprint
from functools import wraps
from recipe import app, db
from . import category
from recipe.models import RecipeCategory, User
from recipe.helpers import key_is_not_empty, login_required, keys_is_not_empty
# from auth.views import api, autho

api_category = Api(category)
resource_fields = {'category_name':fields.String, 'category_id':fields.String}

class Addcategory(Resource):
    @login_required
    def post(self): 
        parser = reqparse.RequestParser()
        #parser.add_argument('userid', type = int)
        #parser.add_argument('category_id', type = int)
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        if keys_is_not_empty(args):

            return {'error': 'all fields must be filled'}, 422
        
        category_name = args['category_name']
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        category = RecipeCategory.query.filter_by(category_name = category_name, user = userid).first()
        #user = token
        # if user is None:
        #     return ({"message": "you are not logged in"})
        #else:
        if category is None:
            #userid = userid
            new_category = RecipeCategory(category_name = category_name, user = userid)
            #userid = userid
            new_category.save_category()
                #response = jsonify({'message': "Recipe category successfully created"})
                #return response
            #return jsonify({"category": new_category})
            response = {'message':"Category created", 'category_name':new_category.category_name}
            return make_response(jsonify(response), 201)
            #return ({'message': "category created", "category_name":new_category.category_name})
        
        else:
            response = ({'message': "Category already exists"})
            return (response, 401)

    
    @login_required
    @marshal_with(resource_fields)
    def get(self):
        #get category details
        response = RecipeCategory.get_all_categories()
        #response = RecipeCategory.query.filter_by(category_name = category_name).first()
        if response is None:
            return jsonify({'message': 'no categories to display'})
        #results = json.loads(response.data)
        #category = RecipeCategory.query.filter_by(category_name = category_name)
        return response
        #return jsonify({'category name': results['category_name'], 'category_id':results['category_id']})
        

class editcategory(Resource):
    '''function to update recipe categories'''
    @login_required
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        category_name = args['category_name']
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'}), 404
        cat.category_name = category_name
        db.session.commit()
        return ({'message':'category edited', 'category name':cat.category_name, 'category_id':category_id}), 200
        
        
class deletecategory(Resource):
    @login_required
    def delete(self, category_id):
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'}), 404
        # category_name = cat.category_name
        # cats = RecipeCategory(category_id, category_name)
        cat_delete = cat.category_name
        db.session.delete(cat)
        db.session.commit()
        
        return ({'message': 'successfully deleted', 'deleted_category': cat_delete}), 200
#api_category.add_resource(Addcategory, '/category')
#
#from categories import category
class search(Resource):
    @login_required
    def get():
        url = 'http://127.0.0.1:5000/search?q=q'
        headers = {'Content-Type': 'application/json'}      
        parser = reqparse.RequestParser()
        parser.add_argument('q', type = str)
        args = parser.parse_args()
        q = args['q']
        filters = [dict(name='category_name', op='like', val='%q%')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(url, params=params, headers=headers)
        assert response.status_code == 200
        print(response.json())
api_category.add_resource(Addcategory, '/category')
#api_category.add_resource(Addcategory, '/category')
api_category.add_resource(editcategory, '/category/<category_id>')
api_category.add_resource(deletecategory, '/category/<category_id>')
app.register_blueprint(category)
