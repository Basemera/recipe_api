import os

from flask_restful import Resource, Api
from api_recipe import create_app
from api_recipe.auth import autho
from api_recipe.categories import category
from api_recipe.recipes import recipe

api = Api()
config_name = os.environ.get('APP_SETTINGS')
app = create_app(config_name)
# api.init_app(app)
# app.register_blueprint(autho)
# app.register_blueprint(category)
# app.register_blueprint(recipe)