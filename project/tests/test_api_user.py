from . import TestConfig
from app.api_views.user import *
import json
import os

class TestUserApi(TestConfig):
	""" tests the user section of the api """

	def test_login(self):
		""" test the login route with admin"""
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')
		
		data = {'phone':admin_phone, 'password':admin_password}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')

		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_login2(self):
		""" test the login route with wrong password"""
		admin_phone = os.getenv('admin_phone')
		
		if not admin_phone:
			raise ValueError('Environment variables not found!')
		
		data = {'phone':admin_phone, 'password':'wrong'}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')

		self.assertTrue(data['message'], 'wrong phone or password')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 401)

	def test_login3(self):
		""" test the login route without parameters"""
		
		data = {}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')

		self.assertTrue(data['message'], 'required data not submitted')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)

