import re
from flask import request, jsonify, make_response, Blueprint
from flask_restful import reqparse, Resource, Api, marshal_with, fields
from api_recipe import db
from api_recipe.models import RecipeCategory, User, Recipes
from api_recipe.helpers import value_is_empty, login_required, valuess_is_empty, is_category_name_valid
from ..helpers import paginate_recipes

# api_recipe = Api(recipe)
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
        # parser = reqparse.RequestParser()
        # parser.add_argument('recipe_name', type = str)
        # parser.add_argument('description', type = str, default='')
        recipe_name = request.data['recipe_name']
        description = request.data['description']
        args = {'recipe_name':recipe_name, 'description':description}
        # args = pathis.props.match.paramsrser.parse_args()
        if valuess_is_empty(args):
            return {'error': 'all fields must be filled'}, 422
        recipes = args['recipe_name']
        description = args['description']
        recipe_name = recipes.strip()
        if recipes.isspace() or recipes!=recipes.strip():
            return ({'message':'no spaces allowed'})
        if not is_category_name_valid(recipes):
            return {'message':'invalid input use format peas'}, 400
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        categories = RecipeCategory.query.filter_by(category_id=category,
                                                    user=userid).first()
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
                response = {'message': 'recipe successfully added',
                                    "category_id":new_recipe.category, 'recipe name':new_recipe.recipe_name, 'description':new_recipe.description}
                return make_response(jsonify(response), 201)
            else:
                return ({"message": "Recipe already exists"}), 409
        return ({'message':'invalid category'}), 404

class getrecipes(Resource):
    """A resource to handle searching of recipes"""
    @login_required
    # @marshal_with(resource_fields)
    def get(self, category):
        """A function to get recipes associated with a category"""
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
        page = page = request.args.get('page', 1, type=int)
        results=[]
        categories = RecipeCategory.query.filter_by(category_id=category, user=userid).first()
        if not categories:
            return ({"message":"category doesnot exist"})
        recipes = Recipes.query.filter_by(user=userid, category=category).all()
        if recipes is None:
            return jsonify({'message':'no recipes to display'}), 404
        items, nex, pagination, previous = paginate_recipes(page, q, userid, category)
        for item in items:
            result1 = {
            'recipe_name':item.recipe_name,
            'recipe_id':item.recipe_id,
            'description':item.description,
            'category':item.category,
            'next':nex,
            'count':pagination.total,
            'previou':previous,
            'pagenumber':pagination.page
        }

            results.append(result1)
        # if results:
        print ({'zzzzzzzz':items})
        # return jsonify({'results':results})
        return ({'results':results, 'count':pagination.total, 'next':nex, 'per_page':pagination.per_page, 'page':pagination.page}, 200)
        # return ({"message":"search item not found"}), 404
        # else:
        #     return recipes, 200


class editrecipe(Resource):
    """A resource to handle updating of recipes"""
    @login_required
    def put(self, recipe_id, category):
        """Function to edit a recipe"""
        # parser = reqparse.RequestParser()
        # parser.add_argument('recipe_name', type = str)
        # parser.add_argument('description', type = str)
        recipe_name= request.data['recipe_name']
        description= request.data['description']
        args = {'recipe_name':recipe_name, 'description':description}
        recipe_name = args['recipe_name'].lower()
        description = args['description']
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        if recipe_name.isspace() or recipe_name!=recipe_name.strip():
            return ({'message':'no spaces allowed'}), 400
        if not is_category_name_valid(recipe_name):
            return {'message':'invalid input use format peas'}, 400
        if not recipe_name or not description:
            return {'message':'all fields required'}, 400
        recipes = Recipes.query.filter_by(recipe_id = recipe_id).first()
        if recipes is not None:
            category = RecipeCategory.query.filter_by(
                category_id=recipes.category,
                user=userid).first()
            if not category:
                return ({"message":"category doesnot exist"}), 404
            recipe2 = Recipes.query.filter_by(
                recipe_name = recipe_name, recipe_id = recipe_id).first()        
            if recipe2:
                recipes.recipe_name = recipe_name
                recipes.description = description
                db.session.commit()
                return ({'recipe name':recipes.recipe_name,
                        'description':recipes.description,
                        'message':'Recipe successfully edited'
                        }
                        ), 200
            # if recipe2.recipe_name == recipe_name:     
            return ({ 'message':'Recipe name already exists'}), 400
        return ({'message':'recipe doesnot exist'}), 404

class delete(Resource):
    def delete(self, category, recipe_id):
        """Function to delete a recipe"""
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        recipe = Recipes.query.filter_by(
            user=userid, category=category, recipe_id =recipe_id).first()
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
    def get(self, category):
        """A function to get recipes"""
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
        results=[]
        if not q:
            return ({"message":"search item not provided"}), 400

        items, nex, pagination, previous = paginate_recipes(page, q, userid, category)
        for item in items:
            result1 = {
            'recipe_name':item.recipe_name,
            'recipe_id':item.recipe_id,
            'next':nex,
            'count':pagination.total,
            'previou':previous,
            'pagenumber':pagination.page
        }

            results.append(result1)
        if results:
            print ({'zzzzzzzz':items})
            # return (results)
            return ({'results':results, 'count':pagination.total, 'next':nex, 'per_page':pagination.per_page, 'page':pagination.page}, 200)
        return ({"message":"search item not found"}), 404
        # if page and per_page is None:
        #     page =1
        #     per_page=2
        
        # recipe_search_query = Recipes.query.filter(
        #     Recipes.recipe_name.ilike('%' + q + '%')).filter_by(
        #         user=userid, category=category).paginate(error_out=False)
        # if recipe_search_query:
        #     results = []
        #     for item in recipe_search_query.items:
        #         recipe_obj = {
        #             "recipe_name": item.recipe_name,
        #             "page_number": recipe_search_query.page,
        #             "items_returned": recipe_search_query.total
        #         }
        #         results.append(recipe_obj)
        # if results:
        #     return results, 200
        # return ({"message":"search item not found"}), 404


# api_recipe.add_resource(Addrecipe, '/category/<category>/recipes')
# api_recipe.add_resource(getrecipes, '/category/<category>/recipes')
# api_recipe.add_resource(editrecipe, '/category/<category>/recipes/<recipe_id>') #category/recipes/<recipe_id>
# api_recipe.add_resource(delete, '/category/<category>/recipes/<recipe_id>') #<category>/recipes/<recipe_id>
# api_recipe.add_resource(search, '/category/<category>/recipes/search')
