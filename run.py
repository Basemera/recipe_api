# #run.py
#from flask import Flask
import os
import unittest
from recipe.auth.views import api
from recipe.categories.views import api_category
from recipe.recipes.views import api_recipe
from recipe import app, db
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
from recipe.config import app_config
#config_name = 'development'
#app = create_app(config_name)
#app = Flask(__name__)
#config_name = os.getenv('APP_SETTINGS') # config_name = "development"
#app = create_app(config_name)

# api.add_resource(AddUser, '/user') # , endpoint = "add_user"
if __name__ == '__main__':
    app.run(debug=True)