import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase
from api_recipe.recipes.views import *
from api_recipe.auth.views import AddUser, api
from api_recipe.categories.views import Addcategory, api_category


class TestRecipesTestCase(BaseTestCase):
    def test_creating_recipes(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h,
                                        data=self.category)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result['message'], 'recipe successfully added')

    def test_token_requirred(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            h = Headers()
            category = self.client.post('/category', headers=h, data=self.category)
            responses = self.client.post('/1/recipes', headers=h, data=self.recipe)
            result = json.loads(responses.data)
            self.assertEqual(responses.status_code, 200)
            self.assertEqual(result['message'], 'token is missing')
 
    def test_token_expired(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            tok1 = 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxN'
            tok2 = 'DU4NjQxNiwiZXhwIjoxNTE0NTkyNDE2fQ.eyJ1c2VyaWQiOjE0fQ'
            tok3 = '.5M0O41VxHuzoU0x43XfgS1yAq6XAD441wlUr-UPMmJE'
            auth = tok1+tok2+tok3
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h,
                                        data=self.category)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'token has expired')


    def test_token_expired(self):
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = 'phiona'
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h,
                                        data=self.category)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'Invalid token')

    def test_duplicate_recipe(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h,
                                        data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h,
                                      data=self.recipe)
            response = self.client.post('/1/recipes',
                                        headers=h, data=self.recipe)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 409)
            self.assertEqual(result['message'], 'Recipe already exists')

    def test_empty_fields(self):
        data = {'recipe_name':'    ', 'description':'beefy'}
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/1/recipes',
                                        headers=h, data=data)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 422)
            self.assertEqual(result['error'], 'all fields must be filled')

    def test_get_all(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            responses = self.client.post('/1/recipes',
                                         headers=h, data=self.recipe)
            response = self.client.get('/1/recipe', headers=h)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('stew', str(result))

    def test_duplicate_recipe(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            result = json.loads(recipe.data)
            self.assertEqual(recipe.status_code, 409)
            self.assertEqual(result['message'], 'Recipe already exists')

    def test_edit_recipe(self):
        data = {"recipe_name":'seafood', 'description':'Smoked over open fire'}
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            response = self.client.post('/1/recipes',
                                        headers=h, data=data)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 201)


    def test_edit_none_existantrecipe(self):
        data = {"recipe_name":'seafood', 'description':'Smoked over open fire'}
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            #token = User.verify_auth_token(auth)
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            response = self.client.put('/recipes/3',
                                       headers=h, data=self.recipe)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(result['message'], 'recipe doesnot exist')

    def test_delete_recipe(self):
        data = {"recipe_name":'seafood', 'description':'Smoked over open fire'}
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            recipe = self.client.post('/1/recipes',
                                      headers=h, data=self.recipe)
            response = self.client.delete('/recipe/1/1', headers=h)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'recipe successfully deleted')

    def test_delete_nonexistantrecipe(self):
        with self.client:
            user = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            created_recipe = self.client.post('/1/recipes',
                                            headers=h, data=self.recipe)
            response = self.client.delete('/recipe/1/3', headers=h)
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(result['message'], 'recipe doesnot exist')

    def test_validate_recipe_name(self):
        data2 ={'username':"Bas", "password":"phiona"}
        data3 = {'recipe_name':1234, 'description':'boiled'}
        with self.client:
            response = self.client.post('/register', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            auth = result['token']
            h = Headers()
            h.add('x-access-token', auth)
            category = self.client.post('/category',
                                        headers=h, data=self.category)
            created_recipe = self.client.post('/1/recipes',
                                              headers=h, data=data3)
            results = json.loads(created_recipe.data)
            self.assertEqual(created_recipe.status_code, 400)
            self.assertEqual(results['message'], 'invalid input use format peas')
            