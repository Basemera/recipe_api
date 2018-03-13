# from flask import request, jsonify, make_response, url_for
# from flask_restful import reqparse, Resource, Api, marshal_with, fields
# from api_recipe import db
# from api_recipe.models import User, RecipeCategory
# from api_recipe.helpers import value_is_empty, login_required, is_category_name_valid, response_with_pagination, paginate_categories
# from . import category

# api_category = Api(category)
# resource_fields = {'category_name':fields.String, 'category_id':fields.String}

# class Addcategory(Resource):
#     """Resource to handle creation of categories """
#     @login_required
#     def post(self):
#         """A method to create a category"""
#         # parser = reqparse.RequestParser()
#         # parser.add_argument('category_name', type = str)
#         category_name = request.data['category_name']
#         args = {'category_name':category_name}
#         category_name = args['category_name']
#         if value_is_empty(args):    
#             return {'error': 'all fields must be filled'}, 422
#         category_name = args['category_name']
#         auth = request.headers.get('x-access-token')
#         userid = User.verify_auth_token(auth)
#         category1 = RecipeCategory.query.filter_by(
#             category_name = category_name, user = userid).first()
#         if category_name.isspace() or category_name!=category_name.strip():
#             return ({'message':'no spaces allowed'})
#         if not is_category_name_valid(category_name):
#             return {'message':'invalid input use format peas'}, 400
#         if category1 is None:
#             new_category = RecipeCategory(category_name = category_name, user = userid)
#             new_category.save_category()
#             response = {'message':"Category created", 
#             'category_name':new_category.category_name}
#             return make_response(jsonify(response), 201)   
#         else:
#             response = ({'message': "Category already exists"})
#             return (response, 401)

#     # @login_required
#     # @marshal_with(resource_fields)
#     # def get(self):
#     #     """A method to get categories created by a user"""
#     #     auth = request.headers.get('x-access-token')
#     #     userid = User.verify_auth_token(auth)
#     #     results = []
#     #     category = RecipeCategory.query.filter_by(user=userid).all()
#     #     if category is []:
#     #         return jsonify({'message':'no categories to display'}), 404
#     #     else:
#     #         return category, 200

#     @login_required
#     # @marshal_with(resource_fields)
#     def get(self):
#         """A method to get categories created by a user"""
#         auth = request.headers.get('x-access-token')
#         userid = User.verify_auth_token(auth)
#         results = []
#         categories = RecipeCategory.query.filter_by(user=userid).all()
        
#         # results.append(result1)
#         if categories is []:
#             return jsonify({'message':'no categories to display'
#                              }), 404
#         else:
#             page = page = request.args.get('page', 1, type=int)
#             q = request.args.get('q', None, type=str)
#             items, nex, pagination, previous = paginate_categories(page, q, userid)
#             for item in items:
#                 result1 = {
#                 'category_name':item.category_name,
#                 'category_id':item.category_id,
#                 'next':nex,
#                 'count':pagination.total,
#                 'previou':previous,
#                 'pagenumber':pagination.page
#             }

#                 results.append(result1)
            
#             return ({'results':results, 'count':pagination.total, 'next':nex}, 200) 
#     #         return response_with_pagination(previous, nex, 0)

# class editcategory(Resource):
#     '''Resource to handle updating categories'''
#     @login_required
#     def put(self, category_id):
#         """Method for updating a category"""
#         category_name = request.data['category_name']
#         args = {'category_name':category_name}
#         # parser = reqparse.RequestParser()
#         # parser.add_argument('category_name', type = str)
#         # args = parser.parse_args()
#         if value_is_empty(args):
#             return {'error': 'all fields must be filled'}, 422
#         category_name = args['category_name']
#         auth = request.headers.get('x-access-token')
#         userid = User.verify_auth_token(auth)
#         cat = RecipeCategory.query.filter_by(user=userid, category_id = category_id).first()
#         if category_name.isspace() or category_name!=category_name.strip():
#             return ({'message':'no spaces allowed'})
#         if not is_category_name_valid(category_name):
#             return {'message':'invalid input'}, 400
#         if cat is None:
#             return ({'message':'category doesnot exist'}), 404
#         new_category = RecipeCategory.query.filter_by(category_name=category_name).first()
#         if new_category:
#             return ({"message":'category name already used please choose another one'}), 400
#         cat.category_name = category_name
#         db.session.commit()
#         return ({'message':'category edited', 'category name':cat.category_name,
#                 'category_id':category_id}), 200
        
        
# class deletecategory(Resource):
#     """A resource to handle the deleting of categories"""
#     @login_required
#     def delete(self, category_id):
#         """Method for deleting categories"""
#         auth = request.headers.get('x-access-token')
#         userid = User.verify_auth_token(auth)
#         cat = RecipeCategory.query.filter_by(user=userid, category_id = category_id).first()
#         if cat is None:
#             return ({'message':'category doesnot exist'}), 404
#         cat_delete = cat.category_name
#         db.session.delete(cat)
#         db.session.commit()
#         return ({'message': 'successfully deleted', 'deleted_category': cat_delete}), 200

# class search(Resource):
#     """A resource to handle the searching for categories"""
#     @login_required
#     def get(self):
#         """Method to search for categories by name"""
#         results=[]
#         auth = request.headers.get('x-access-token')
#         userid = User.verify_auth_token(auth)
#         parser = reqparse.RequestParser()
#         parser.add_argument('q', type = str)
#         parser.add_argument('per_page', type = int, default=2)
#         parser.add_argument('page', type = int, default=1)
#         # q = request.data['q']
#         # per_page = request.data['per_page']
#         # page = request.data['page']
#         # args = {'q':q, 'per_page':per_page, 'page':page}
#         args = parser.parse_args()
#         q = args['q']
#         per_page = args['per_page']
#         page = args['page']
#         if not q:
#             return ({"message":"search item not provided"}), 400
#         items, nex, pagination, previous = paginate_categories(page, q, userid)
#         for item in items:
#             result1 = {
#             'category_name':item.category_name,
#             'category_id':item.category_id,
#             'next':nex,
#             'count':pagination.total,
#             'previou':previous,
#             'pagenumber':pagination.page
#         }

#             results.append(result1)
#         if results:
#             print ({'zzzzzzzz':items})
#             # return (results)
#             return ({'results':results, 'count':pagination.total, 'next':nex, 'per_page':pagination.per_page, 'page':pagination.page}, 200)
#         return ({"message":"search item not found"}), 404
        
        
#         # category_search_query = RecipeCategory.query.filter(
#         #     RecipeCategory.category_name.ilike('%' + q + '%')).filter_by(
#         #         user=userid).paginate(error_out=False)
#         # if category_search_query:
#         #     results = []
#         #     for item in category_search_query.items:
#         #         recipe_obj = {
#         #             "category_name": item.category_name,
#         #             "page_number": category_search_query.page,
#         #             "items_returned": category_search_query.total
#         #         }
#         #         results.append(recipe_obj)
#         # if results:
#         #     return results, 200
#         # return ({"message":"search item not found"}), 404

# api_category.add_resource(Addcategory, '/category')
# api_category.add_resource(search, '/category/search')
# api_category.add_resource(editcategory, '/category/<category_id>')
# api_category.add_resource(deletecategory, '/category/<category_id>')

