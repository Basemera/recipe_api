import sys
import json
from flask import Flask, request, jsonify, g, json, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, marshal_with, fields
from flask import abort, g, jsonify, Blueprint
from functools import wraps
from recipe import app, db
from . import category
from recipe.models import RecipeCategory, User
from recipe.helpers import key_is_not_empty, login_required, keys_is_not_empty
# from auth.views import api, autho

api_category = Api(category)
resource_fields = {'category_name':fields.String, 'category_id':fields.String}
import re
def is_category_name_valid(category_name):
    if re.match("^[A-Za-z_-]*$", category_name):
        return True
    return False

class Addcategory(Resource):
    @login_required
    def post(self): 
        parser = reqparse.RequestParser()
        #parser.add_argument('userid', type = int)
        #parser.add_argument('category_id', type = int)
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        if keys_is_not_empty(args):

            return {'error': 'all fields must be filled'}, 422
        
        category_name = args['category_name']
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        category = RecipeCategory.query.filter_by(category_name = category_name, user = userid).first()
        
        if not is_category_name_valid(category_name):
            return {'message':'invalid input use format peas'}, 400
        if category is None:
            #userid = userid
            new_category = RecipeCategory(category_name = category_name, user = userid)
            #userid = userid
            new_category.save_category()
                #response = jsonify({'message': "Recipe category successfully created"})
                #return response
            #return jsonify({"category": new_category})
            response = {'message':"Category created", 'category_name':new_category.category_name}
            return make_response(jsonify(response), 201)
            #return ({'message': "category created", "category_name":new_category.category_name})
        
        else:
            response = ({'message': "Category already exists"})
            return (response, 401)

   
    @login_required
    @marshal_with(resource_fields)
    def get(self):
        auth = request.headers.get('x-access-token')
        userid = User.verify_auth_token(auth)
        
        cat = RecipeCategory.query.filter_by(user=userid).all()
        if cat is None:
            return jsonify({'message':'no categories to display'})
        #categories = RecipeCategory.get_all_categories()
        else:
            return cat
        # else:
        #     return jsonify({'message':'no categories to display'})

        #result = categories.filter_by(user=userid)
        # if cat is None:
        #     return jsonify({'message':'no categories to display'})
        
        # return cat
    #     auth = request.headers.get('x-access-token')
    #    #user_id = user.id
    #     userid = User.verify_auth_token(auth)
    #     q = request.args.get('q', '')
    #     per_page = request.args.get('per_page', '')
    #     page = request.args.get('page', '')

    #     if not q:
    #         response= ({"message": "Search item not provided"})
    #         return make_response(jsonify(response)), 200
    #     results = []
    #     recipe_search_query = RecipeCategory.query.filter(RecipeCategory.category_name.ilike('%' + q + '%')).filter_by(user=userid).paginate(per_page=10, page=1, error_out=False)
    #     if not recipe_search_query:
    #         response = "Category doesnot exist"
    #         return make_response(jsonify(response))
    #     for category in recipe_search_query.items:
    #         cat_obj = {
    #             "name": category.category_name,
    #             "page_number": recipe_search_query.page,
    #             "items_returned": recipe_search_query.total
    #         }
    #         results.append(cat_obj)
    #     return make_response(jsonify(results))
        # if not recipe_search_query:
        #     response= {"message": "Search item not found"}
        #     return make_response(jsonify(response)), 200
        
        # else: 
        #     results = results.append(recipe_search_query)
        #     return results
        
            # search_categories=RecipeCategory.query.filter(RecipeCategory.category_name.ilike('%' + q + '%'))
        

        # if q:
        #     for item in result:
        #         if q in result.category_name:
        #           results.append(item)
        #           return results
        
            #return jsonify({'error':'no categories exist'})
        #return jsonify({'error':'no categories exist'})


        

class editcategory(Resource):
    '''function to update recipe categories'''
    @login_required
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_name', type = str)
        args = parser.parse_args()
        category_name = args['category_name']
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'}), 404
        cat.category_name = category_name
        db.session.commit()
        return ({'message':'category edited', 'category name':cat.category_name, 'category_id':category_id}), 200
        
        
class deletecategory(Resource):
    @login_required
    def delete(self, category_id):
        cat = RecipeCategory.query.filter_by(category_id = category_id).first()
        if cat is None:
            return ({'message':'category doesnot exist'}), 404
        # category_name = cat.category_name
        # cats = RecipeCategory(category_id, category_name)
        cat_delete = cat.category_name
        db.session.delete(cat)
        db.session.commit()
        
        return ({'message': 'successfully deleted', 'deleted_category': cat_delete}), 200
#api_category.add_resource(Addcategory, '/category')
#
#from categories import category
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
        
        
        
        recipe_search_query = RecipeCategory.query.filter(RecipeCategory.category_name.ilike('%' + q + '%')).filter_by(user=userid).paginate(per_page=10, page=1, error_out=False)
        if recipe_search_query:
            # # response = "Category doesnot exist"
            # return ({"message":"search item not found"}), 404
            # #return make_response(jsonify(response))
            for item in recipe_search_query.items:
                cat_obj = {
                    "name": item.category_name,
                    "page_number": recipe_search_query.page,
                    "items_returned": recipe_search_query.total
                }
                results = []
                results.append(cat_obj)
                return make_response(jsonify(results),200)
        return ({"message":"search item not found"}), 404
        # if not recipe_search_query:
        #     response= {"message": "Search item not found"}
        #     return make_response(jsonify(response)), 200
        
        # else: 
        #     results = results.append(recipe_search_query)
        #     return results
        
        # auth = request.headers.get('x-access-token')
        # userid = User.verify_auth_token(auth)
        # q = request.args.get('q', "")
        # per_page = int(request.args.get('per_page'))
        # page = int(request.args.get('page'))
        # results = []
        # if q is not None:
        # #     response= ({"message": "Search item not provided"})
        # #     return make_response(jsonify(response)), 200
            
        #     #recipe_search_query = RecipeCategory.query.filter(RecipeCategory.category_name.like('%' + q.strip() + '%')).filter_by(user=userid).paginate(per_page=per_page, page=page, error_out=False).recipes
        #     recipe_search_query = RecipeCategory.query.filter(RecipeCategory.category_name.like('%' + q.strip() + '%')).filter_by(user=userid).paginate(per_page, page, False)

        #     return recipe_search_query
        # # else:
        # #     recipe_search_query = RecipeCategory.query.filter(RecipeCategory.category_name.like('%' + q.strip() + '%')).filter_by(user=userid).paginate(per_page=per_page, page=page, error_out=False).recipes

        # if not recipe_search_query:
        #      response = "Category doesnot exist"
        #      return make_response(jsonify(response))
        # for category in recipe_search_query.items:
        #     cat_obj = {
        #         "name": category.category_name,
        #         "page_number": recipe_search_query.page,
        #         "items_returned": recipe_search_query.total
        #     }
        #     results.append(cat_obj)
        # print(results)
        # return make_response(jsonify({results})), 201

api_category.add_resource(Addcategory, '/category')
api_category.add_resource(search, '/category/search')
api_category.add_resource(editcategory, '/category/<category_id>')
api_category.add_resource(deletecategory, '/category/<category_id>')
app.register_blueprint(category)
