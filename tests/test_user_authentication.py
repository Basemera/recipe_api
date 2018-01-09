import unittest
import json
from flask import jsonify, json
from flask_testing import TestCase
from recipe import db
from recipe.models import User
from recipe.auth.views import AddUser, api
from werkzeug.datastructures import Headers
from tests.base import BaseTestCase

class TestUserAuthenticationTestCase(BaseTestCase):
    def test_user_login(self):
        with self.client:
            response = self.client.post('/user', data=self.user)
            responses = self.client.post('/login', data=self.data2)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 200)
            self.assertEqual(result['message'], 'You have successfully logged in')
            self.assertTrue(result['token'])

    def test_incorrect_credentials(self):
        with self.client:
            data = {'username':'Bas', 'password':'phiona19876650e4'}
            response = self.client.post('/user', data=self.user)
            responses = self.client.post('/login', data=data)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'invalid credentials')

    def test_nonexistent_user(self):
        data2 = {'username':"Basph", "password":"phiona"}
        with self.client:
            response = self.client.post('/user', data=self.user)
            self.assertEqual(response.status_code, 201)
            responses = self.client.post('/login', data=data2)
            result = json.loads(responses.data.decode())
            self.assertEqual(responses.status_code, 401)
            self.assertEqual(result['message'], 'user doesnot exist')

    def test_log_out(self):
        with self.client:
            register_user = self.client.post('/user', data=self.user)
            log_in = self.client.post('/login', data=self.data2)
            results = json.loads(log_in.data.decode())
            auth = results['token']
            h = Headers()
            h.add('x-access-token', auth)
            response = self.client.post('/logout', headers=h)
            result = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['message'], 'logged out')
