import re
from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with, fields
from flask import abort, g, jsonify, Blueprint
from functools import wraps
from recipe import app, db
from . import recipe
from recipe.models import RecipeCategory, User, Recipes
from recipe.helpers import value_is_empty, login_required, valuess_is_empty


api_recipe = Api(recipe)
resource_fields = {'recipe_name':fields.String,
                   'description':fields.String,
                   'category':fields.String,
                   'recipe_id':fields.Integer
}

def is_recipe_name_valid(recipe_name):
    """function to validate the recipe name"""
    if re.match("^[A-Za-z_-]*$", recipe_name):
        return True
    return False

def is_description_valid(description):
    if re.match("^[A-Za-z_-]*$", description):
        return True
    return False

class Addrecipe(Resource):
    """Resource to handle creating recipes"""
    @login_required
    def post(self, category):
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_name', type = str)
        parser.add_argument('description', type = str, default='')
        args = parser.parse_args()
        if valuess_is_empty(args):
            return {'error': 'all fields must be filled'}, 422
        recipe_name = args['recipe_name'].lower()
        description = args['description']
        if not is_recipe_name_valid(recipe_name):
            return {'message':'invalid input use format peas'}, 400
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        categories = RecipeCategory.query.filter_by(category_id=category, user=userid).first()
        if categories:
            recipes = Recipes.query.filter_by(
                user = userid,
                category=category,
                recipe_name = recipe_name
                ).first()
            if recipes is None:
                category = category
                user = userid
                new_recipe = Recipes(recipe_name, description, user, category)
                new_recipe.save_recipe()
                response = jsonify({'message': 'recipe successfully added',
                                    "category_id":new_recipe.category})
                return response

            else:

                return ({"message": "Recipe already exists"}), 409
        return ({'message':'invalid category'})
class getrecipes(Resource):
    """A resource to handle searching of recipes"""
    @login_required
    @marshal_with(resource_fields)
    def get(self, category):
        """A function to get recipes associated with a category"""
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        categories = RecipeCategory.query.filter_by(category_id=category, user=userid).first()
        if not categories:
            return ({"message":"category doesnot exist"})
        recipes = Recipes.query.filter_by(user=userid, category=category).all()
        if recipes is None:
            return jsonify({'message':'no recipes to display'})
        else:
            return recipes


class editrecipe(Resource):
    """A resource to handle updating of recipes"""
    @login_required
    def put(self, recipe_id):
        """Function to edit a recipe"""
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_name', type = str)
        parser.add_argument('description', type = str)
        args = parser.parse_args()
        recipe_name = args['recipe_name'].lower()
        description = args['description']
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        
        recipes = Recipes.query.filter_by(recipe_id = recipe_id).first()
        if recipes is not None:
            category = RecipeCategory.query.filter_by(category_id=recipes.category, user=userid).first()
            if not category:
                return ({"message":"category doesnot exist"})
            recipe2 = Recipes.query.filter_by(recipe_name = recipe_name).first()
            if recipe2 is None:
                recipe.recipe_name = recipe_name
                recipe.description = description
                db.session.commit()
                return ({'recipe name':recipe.recipe_name,
                        'description':recipe.description})
            return ({ 'message':'Recipe name already exists'})
        return ({'message':'recipe doesnot exist'}), 404

class delete(Resource):
    def delete(self, category, recipe_id):
        """Function to delete a recipe"""
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        recipe = Recipes.query.filter_by(user=userid, category=category, recipe_id =recipe_id).first()

        if recipe is None:
            return ({'message':'recipe doesnot exist'}, 404)
        db.session.delete(recipe)
        db.session.commit()
        recipe_delete = recipe.recipe_name
        return ({'message': 'recipe successfully deleted',
                'recipe name':recipe_delete}), 200


class search(Resource):
    """A resource to handle searching of recipes"""
    @login_required
    def get(self):
        """A function to get recipes"""
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        parser = reqparse.RequestParser()
        parser.add_argument('category', type = int)
        parser.add_argument('q', type = str)
        parser.add_argument('per_page', default=2)
        parser.add_argument('page', default=1)
        args = parser.parse_args()
        category = args['category']
        q = args['q']
        per_page = args['per_page']
        page = args['page']
        if not category:
            return ({'message':'category not provided'}), 400
        if not q:
            return ({"message":"search item not provided"}), 400

        if page and per_page is None:
            page =1
            per_page=2
        
        recipe_search_query = Recipes.query.filter(Recipes.recipe_name.ilike('%' + q + '%')).filter_by(user=userid, category=category).paginate(per_page=10, page=1, error_out=False)
        if recipe_search_query:
            results = []
            for item in recipe_search_query.items:
                recipe_obj = {
                    "name": item.recipe_name,
                    "page_number": recipe_search_query.page,
                    "items_returned": recipe_search_query.total
                }
                results.append(recipe_obj)
            return make_response(jsonify(results), 200)
        return ({"message":"search item not found"}), 404


api_recipe.add_resource(Addrecipe, '/<category>/recipes')
api_recipe.add_resource(getrecipes, '/<category>/recipe')
api_recipe.add_resource(editrecipe, '/recipes/<recipe_id>')
api_recipe.add_resource(delete, '/recipe/<category>/<recipe_id>')# /categories/<category_id>/recipes/<recipe_id>
api_recipe.add_resource(search, '/recipes/search')

app.register_blueprint(recipe)

