from flasgger import Swagger
# from recipe_api import create_app
# from api_recipe.auth.views import api
# from api_recipe.categories.views import api_category
# from api_recipe.recipes.views import api_recipe
from api_recipe import app
# app = create_app('development')
# swagger = Swagger(app)
if __name__ == '__main__':
    app.run(debug=True)