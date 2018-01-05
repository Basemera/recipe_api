import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import app, db
from recipe.models import User
#from app.app import app, db
from recipe.auth.views import AddUser, api
#from app.views import AddUser
from werkzeug.datastructures import Headers
from base64 import b64encode
from tests.base import BaseTestCase

class TestUserAuthenticationTestCase(BaseTestCase):
    def test_user_login(self):
        data2 ={'username':"Bas", "password":"phiona"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            self.assertEqual(response.status_code, 201)
            responses = self.client.post('/login', data = self.data2)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 200)
            self.assertEqual(result['message'], 'You have successfully logged in')
            self.assertTrue(result['token'])

    def test_incorrect_credentials(self):
        data2 ={'username':"Bas", "password":"phi"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            self.assertEqual(response.status_code, 201)
            responses = self.client.post('/login', data = data2)
            result = json.loads(responses.data.decode())

            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'invalid credentials')

    def test_nonexistent_user(self):
        data2 ={'username':"Basph", "password":"phiona"}
        with self.client:
            response = self.client.post('/user', data = self.user)
            self.assertEqual(response.status_code, 201)
            responses = self.client.post('/login', data = data2)

            result = json.loads(responses.data.decode())

            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'user doesnot exist')