import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from api_recipe import db, create_app
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase
from api_recipe.recipes.views import *
from api_recipe.auth.views import AddUser, api
from api_recipe.categories.views import Addcategory, api_category

class TestRecipeSearchTestCase(BaseTestCase):
    def test_get_all_recipes(self):
        data = {'category_name':'eggs'}
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            search = self.client.get('/1/recipes', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_search_none_existing_recipe(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            search = self.client.get(
                '/1/recipes/search?q=fried&per_page=2&page=1',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 404)
            self.assertEqual(result['message'], 'search item not found')
    def test_search_no_search_parameter_provided(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            response = self.client.post('/recipe',
                                        headers=h, data=self.recipe)
            search = self.client.get(
                '/1/recipes/search?q=&per_page=k&page=1',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(result['message'], 'search item not provided')

    
    def test_get_all_recipes_for_a_user(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            search = self.client.get('/1/recipes', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_page_parameter_provided_is_string(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            search = self.client.get(
                '/1/recipes/search?q=stew&per_page=2&page=k',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_page_parameter_not_gven(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers = h, data = self.category)
            recipe = self.client.post('/1/recipes',
                                    headers = h, data = self.recipe)
            search = self.client.get(
                '/1/recipes/search?q=stew&per_page=2&page=',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def test_per_page_parameter_provided_is_string(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            search = self.client.get(
                '/1/recipes/search?q=stew&per_page=k&page=1',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            self.assertIn('stew', str(result))
    def test_per_page_parameter_not_gven(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category',
                                    headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            search = self.client.get(
                '/1/recipes/search?q=stew&per_page=&page=1',
                headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
    def testgetallcategoriesforauser(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            logged_in = self.client.post('/login', data=self.data2)
            result = json.loads(logged_in.data)
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            resp = self.client.post('/category', headers=h, data=self.category)
            search = self.client.get('/category', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            