import sys
import json
from flask import Flask, request, jsonify, g, json, abort, make_response, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with, fields
from functools import wraps
from recipe import app, db
from . import category
from recipe.models import RecipeCategory, User
from recipe.helpers import value_is_empty, login_required, is_category_name_valid

api_category = Api(category)
resource_fields = {'category_name':fields.String, 'category_id':fields.String}


class Addcategory(Resource):
    """Resource to handle creation of categories """
    @login_required
    def post(self):
        """A method to create a category"""
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        if value_is_empty(args):

            return {'error': 'all fields must be filled'}, 422
        
        category_name = args['category_name']
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        category = RecipeCategory.query.filter_by(category_name = category_name, user = userid).first()
        
        if not is_category_name_valid(category_name):
            return {'message':'invalid input use format peas'}, 400
        if category is None:
            new_category = RecipeCategory(category_name = category_name, user = userid)
            new_category.save_category()
            response = {'message':"Category created", 'category_name':new_category.category_name}
            return make_response(jsonify(response), 201)
        
        else:
            response = ({'message': "Category already exists"})
            return (response, 401)

   
    @login_required
    @marshal_with(resource_fields)
    def get(self):
        """A method to get categories created by a user"""
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        
        cat = RecipeCategory.query.filter_by(user=userid).all()
        if cat is None:
            return jsonify({'message':'no categories to display'})
        else:
            return cat


        

class editcategory(Resource):
    '''Resource to handle updating categories'''
    @login_required
    def put(self, category_id):
        """Method for updating a category"""
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        if value_is_empty(args):
            return {'error': 'all fields must be filled'}, 422
        category_name = args['category_name']
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'}), 404
        cat.category_name = category_name
        db.session.commit()
        return ({'message':'category edited', 'category name':cat.category_name, 'category_id':category_id}), 200
        
        
class deletecategory(Resource):
    """A resource to handle the deleting of categories"""
    @login_required
    def delete(self, category_id):
        """Method for deleting categories"""
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'}), 404
        cat_delete = cat.category_name
        db.session.delete(cat)
        db.session.commit()
        
        return ({'message': 'successfully deleted', 'deleted_category': cat_delete}), 200

class search(Resource):
    """A resource to handle the searching for categories"""
    @login_required
    def get(self):
        """Method to search for categories by name"""
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        parser = reqparse.RequestParser()
        parser.add_argument('q', type = str)
        parser.add_argument('per_page', default=2)
        parser.add_argument('page', default=1)
        args = parser.parse_args()
        q = args['q']
        per_page = args['per_page']
        page = args['page']
        
        if not q:
            response= {"message": "Search item not provided"}
            return ({"message":"search item not provided"}), 400
        if page and per_page is None:
            page =1
            per_page=2
        
        recipe_search_query = RecipeCategory.query.filter(RecipeCategory.category_name.ilike('%' + q + '%')).filter_by(user=userid).paginate(per_page=10, page=1, error_out=False)
        if recipe_search_query:
            for item in recipe_search_query.items:
                cat_obj = {
                    "name": item.category_name,
                    "page_number": recipe_search_query.page,
                    "items_returned": recipe_search_query.total
                }
                results = []
                results.append(cat_obj)
                return make_response(jsonify(results),200)
        return ({"message":"search item not found"}), 404

api_category.add_resource(Addcategory, '/category')
api_category.add_resource(search, '/category/search')
api_category.add_resource(editcategory, '/category/<category_id>')
api_category.add_resource(deletecategory, '/category/<category_id>')
app.register_blueprint(category)
