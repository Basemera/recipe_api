from flask import Blueprint
from flask_restful import Api
from .views import Addrecipe, getrecipes, editrecipe, delete, search

"""Creating Blueprints for the login and user"""

recipe = Blueprint('recipe', __name__)
api_recipe = Api(recipe)

api_recipe.add_resource(Addrecipe, '/category/<category>/recipes')
api_recipe.add_resource(getrecipes, '/category/<category>/recipes')
api_recipe.add_resource(editrecipe, '/category/<category>/recipes/<recipe_id>') #category/recipes/<recipe_id>
api_recipe.add_resource(delete, '/category/<category>/recipes/<recipe_id>') #<category>/recipes/<recipe_id>
api_recipe.add_resource(search, '/category/<category>/recipes/search')
