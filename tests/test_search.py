import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, db
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase
from recipe.recipes.views import *
from recipe.auth.views import AddUser, api
from recipe.categories.views import Addcategory, api_category


class TestSearchTestCase(BaseTestCase):
    def testsearchcategories(self):
        data2 ={'username':"Bas", "password":"phiona1984"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            print (result)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search?q=fish&per_page=2&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            

    def testsearchnoneexistingcategory(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search?q=peas&per_page=2&page=1', headers=h)
        
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 404)
            self.assertEqual(result['message'], 'search item not found')
            

    def testsearchnosearchparameterprovided(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(result['message'], 'search item not provided')

    def testpageparameternotprovided(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search?q=fish&per_page=2&page=', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            # self.assertEqual(result['message'], 'search item not provided')

    def testpageparameterprovidedisstring(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search?q=fish&per_page=2&page=k', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)

    def testper_pageparameternotprovided(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search?q=fish&per_page=&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            # self.assertEqual(result['message'], 'search item not provided')

    def testpageparameterprovidedisstring(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
           
            search = self.client.get('/category/search?q=fish&per_page=k&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)


    def testgetallcategoriesforauser(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            
           
            search = self.client.get('/category', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)




class TestRecipeSearchTestCase(BaseTestCase):
    def testgetallrecipes(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            response = self.client.post('/recipe', headers = h, data=self.recipe)
           
            search = self.client.get('/recipes', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            

    def testsearchnoneexistingrecipe(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            response = self.client.post('/recipe', headers = h, data=self.recipe)
           
            search = self.client.get('/recipes/search?q=fried&per_page=2&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 404)
            self.assertEqual(result['message'], 'search item not found')
            

    def testsearchnosearchparameterprovided(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            response = self.client.post('/recipe', headers = h, data=self.recipe)
           
            search = self.client.get('/recipes/search?q=&per_page=k&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(result['message'], 'search item not provided')

    def testsearchnocategoryprovided(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            response = self.client.post('/recipe', headers = h, data=self.recipe)
           
            search = self.client.get('/recipes/search?q=p&per_page=k&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(result['message'], 'category not provided')

    def testsearchcategoryprovidedisnotinterger(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            response = self.client.post('/recipe', headers = h, data=self.recipe)
           
            search = self.client.get('/recipes/search?q=p&per_page=k&page=1&category=', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 400)
            self.assertEqual(result['message'], {'category': "invalid literal for int() with base 10: ''"})

    def testgetallrecipesforauser(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            response = self.client.post('/recipe', headers = h, data=self.recipe)
           
            search = self.client.get('/recipes', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)


    def testpageparameterprovidedisstring(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            recipe = self.client.post('/1/recipe', headers = h, data = self.recipe)
            search = self.client.get('/recipes/search?q=stew&per_page=2&page=k', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)

    def testpageparameternotgven(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            recipe = self.client.post('/1/recipe', headers = h, data = self.recipe)
            search = self.client.get('/recipes/search?q=stew&per_page=2&page=', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)

    def testper_pageparameterprovidedisstring(self):
            data2 ={'username':"Bas", "password":"phiona"}
            data = {'recipe_name':"stew", 'description':"prepared with water"}
            #self.client = app.test_client()
            with self.client:
                user = self.client.post('/user', data=self.user)
                logged_in = self.client.post('/login', data = self.data2)

                result = json.loads(logged_in.data)
                auth = result['token']
        
                h = Headers()
                h.add('x-access-token', auth)
            
                resp = self.client.post('/category', headers = h, data = self.category)
                recipe = self.client.post('/1/recipe', headers = h, data = self.recipe)
                search = self.client.get('/recipes/search?q=stew&per_page=k&page=1', headers=h)
                result = json.loads(search.data)
                self.assertEqual(search.status_code, 200)
                # self.assertEqual(result['message'], 'search item not found')
    def testper_pageparameternotgven(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            recipe = self.client.post('/1/recipe', headers = h, data = self.recipe)
            search = self.client.get('/recipes/search?q=stew&per_page=&page=1', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)

    def testgetallcategoriesforauser(self):
        data2 ={'username':"Bas", "password":"phiona"}
        #self.client = app.test_client()
        with self.client:
            user = self.client.post('/user', data=self.user)
            logged_in = self.client.post('/login', data = self.data2)

            result = json.loads(logged_in.data)
            auth = result['token']
    
            h = Headers()
            h.add('x-access-token', auth)
        
            resp = self.client.post('/category', headers = h, data = self.category)
            
           
            search = self.client.get('/category', headers=h)
            result = json.loads(search.data)
            self.assertEqual(search.status_code, 200)
            

    # def testsearchnosearchpageparameternotintergerprovided(self):
    #     data2 ={'username':"Bas", "password":"phiona"}
    #     #self.client = app.test_client()
    #     with self.client:
    #         user = self.client.post('/user', data=self.user)
    #         logged_in = self.client.post('/login', data = data2)

    #         result = json.loads(logged_in.data)
    #         auth = result['token']
    
    #         h = Headers()
    #         h.add('x-access-token', auth)
        
    #         resp = self.client.post('/category', headers = h, data = self.category)
           
    #         search = self.client.get('/category/search?q=peas&per_page=t&page=t', headers=h)
    #         result = json.loads(search.data)
    #         self.assertEqual(search.status_code, 200)
    #         self.assertEqual(result['error'], 'you must specify an interger')
    #  