from flasgger import Swagger
from recipe import create_app
# from recipe_api import create_app
from recipe.auth.views import api
from recipe.categories.views import api_category
from recipe.recipes.views import api_recipe
from recipe import create_app, db
from instance.config import app_config
app = create_app('development')
# app = create_app(app_config['development'])
swagger = Swagger(app)
if __name__ == '__main__':
    app.run(debug=True)