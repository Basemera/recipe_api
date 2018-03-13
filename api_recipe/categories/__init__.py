from flask import Blueprint
from flask_restful import Api
from .views import Addcategory, search, editcategory, deletecategory


"""Creating Blueprints for the login and user"""

category = Blueprint('category', __name__)
api_category = Api(category)

api_category.add_resource(Addcategory, '/category')
api_category.add_resource(search, '/category/search')
api_category.add_resource(editcategory, '/category/<category_id>')
api_category.add_resource(deletecategory, '/category/<category_id>')
