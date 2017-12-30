from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with, fields
from flask import abort, g, jsonify, Blueprint
from functools import wraps
from recipe import app, db
from . import recipe
from recipe.models import RecipeCategory, User, Recipes
from recipe.helpers import key_is_not_empty, login_required, keyss_is_not_empty


api_recipe = Api(recipe)
resource_fields = {'recipe_name':fields.String, 'description':fields.String, 'category':fields.String}
import re
def is_recipe_name_valid(recipe_name):
    if re.match("^[A-Za-z_-]*$", recipe_name):
        return True
    return False

def is_description_valid(description):
    if re.match("^[A-Za-z_-]*$", description):
        return True
    return False

class Addrecipe(Resource):
    """Function to create recipes"""
    @login_required
    #@marshal_with(resource_fields)
    def post(self, category): 
        parser = reqparse.RequestParser()
        #parser.add_argument('recipe_id', type = int)
        parser.add_argument('recipe_name', type = str)
        parser.add_argument('description', type = str, default='')
        args = parser.parse_args()
        if keyss_is_not_empty(args):

            return {'error': 'all fields must be filled'}, 422
        #recipe_id = args['recipe_id']
        recipe_name = args['recipe_name']
        description = args['description']
        if not is_recipe_name_valid(recipe_name):
            return {'message':'invalid input use format peas'}, 400
        # if not is_description_valid(description):
        #     return {'message':'invalid input use format peas'}, 400
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)

        recipe = Recipes.query.filter_by(recipe_name = recipe_name, user = userid, category = category).first()
        if recipe is None:
            category = category
            user = userid
            #user = RecipeCategory.query.filter_by(category_id = category_id).first()
            #userid = user.userid
            new_recipe = Recipes(recipe_name, description, user, category)
            new_recipe.save_recipe()
            response = jsonify({'message': 'recipe successfully added', "category_id":new_recipe.category})
            return response
            
        else:
            
            return ({"message": "Recipe already exists"}), 409
class getrecipes(Resource):
    @login_required
    @marshal_with(resource_fields)
    def get(self):
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        
        recipe = Recipes.query.filter_by(user=userid).all()
        if recipe is None:
            return jsonify({'message':'no recipes to display'})
        #categories = RecipeCategory.get_all_categories()
        else:
            return recipe
        

class editrecipe(Resource):
    '''function to update recipes'''
    @login_required
    def put(self, recipe_id):
        parser = reqparse.RequestParser()
        parser.add_argument('recipe_name', type = str)
        parser.add_argument('description', type = str)
        args = parser.parse_args()
        recipe_name = args['recipe_name']
        description = args['description']

        recipe = Recipes.query.filter_by(recipe_id = recipe_id).first()
        if recipe is None:
            return ({'message':'recipe doesnot exist'}), 404
        recipe.recipe_name = recipe_name
        recipe.description = description
        db.session.commit()
        return ({'recipe name':recipe.recipe_name, 'description':recipe.description})
        # parser = reqparse.RequestParser()
        # parser.add_argument('recipe_name', type = str)
        # parser.add_argument('description', type = str)
        # args = parser.parse_args()
        # recipe_name = args['recipe_name']
        # description = args['description']

        # recipe = Recipes.query.filter_by(recipe_id = recipe_id).first()
        # if recipe is None:
        #     return ({'message':'recipe doesnot exist'})

        # if recipe_name or description is None:
        #     recipe_name = recipe.recipe_name
        #     # recipe.name = recipe.recipe_name
        #     description = recipe.description
        # recipe_name = args['recipe_name']
        # description = args['description']
        # # recipe.category = recipe.category
        # # recipe.user = recipe.user
        # # new_recipe = Recipes(recipe_name, description, user, category)
        # # new_recipe.save_recipe()
        # # new_recipe = Recipes(recipe_name, description)
        # db.session.commit()
        # return ({'message':'successfully updated', 'recipe name':recipe.recipe_name, 'description':recipe.description})
        
        
# class deleterecipe(Resource):
#     @login_required
    def delete(self, recipe_id):
        recipe = Recipes.query.filter_by(recipe_id =recipe_id).first()
        
        if recipe is None:
            return ({'message':'recipe doesnot exist'}, 404)
        db.session.delete(recipe)
        db.session.commit()
        recipe_delete = recipe.recipe_name
        return ({'message': 'recipe successfully deleted', 'recipe name':recipe_delete}), 200

# class getrecipes(Resource):
#     @login_required
#     def get(self, name):
#         recipe = Recipes.query.join(RecipeCategory).filter(Recipes.name==name).all()
#         #recipe = Recipes.query.has(RecipeCategory.category_id = category_id).all()
#         if recipe:
#             schema = UserSchema(many = True)
#             result = schema.dump(recipe)
#             return ({"recipe":result.data})
#             #return output_json(recipe, 200)
#             # data = {'name':Recipes.name}
#             #return ({'message':"recipe exists"})
#             #return jsonify({"recipes":recipe})
#         return jsonify({"recipes":"doesnot exist"})

class search(Resource):
    @login_required
    def get(self):
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
        # q = request.args.get('q', '')
        # per_page = request.args.get('per_page')
        # page = request.args.get('page')
        
        if not q:
            response= {"message": "Search item not provided"}
            return ({"message":"search item not provided"}), 400
            #return make_response(response), 200

        if page and per_page is None:
            page =1
            per_page=2

        # if type(per_page)!= int and type(page)!=int:
        #     return ({"error":"you must specify an interger"})
        
        results = []
        recipe_search_query = Recipes.query.filter(Recipes.recipe_name.ilike('%' + q + '%')).filter_by(user=userid).paginate(per_page=10, page=1, error_out=False)
        if recipe_search_query:
            
            #return make_response(jsonify(response))
            for item in recipe_search_query.items:
                recipe_obj = {
                    "name": item.recipe_name,
                    "page_number": recipe_search_query.page,
                    "items_returned": recipe_search_query.total
                }
                results.append(recipe_obj)
                return make_response(jsonify(results), 200)

        response = " doesnot exist"
        return ({"message":"search item not found"}), 404


api_recipe.add_resource(Addrecipe, '/<category>/recipes')
api_recipe.add_resource(getrecipes, '/recipes')
api_recipe.add_resource(editrecipe, '/recipes/<recipe_id>')
api_recipe.add_resource(search, '/recipes/search')

app.register_blueprint(recipe)

