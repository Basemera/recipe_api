import os

from api_recipe import create_app

config_name = os.environ.get('APP_SETTINGS')
app = create_app(config_name)