from . import TestConfig
from app.api_views.person import *
import json
import os

class TestPersonApi(TestConfig):

	def test_addage(self):
		""" login as admin then add new age"""

		# admin
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

		# add new age

		headers = {'token':data['data']['token']}
		data = {'minage':40, 'maxage':50}


		# post requset
		result = self.client_app.post("/api/addage", data=json.dumps(data), headers=headers,\
									content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')		
		self.assertEqual(data['message'],  None)
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

	def test_addage2(self):
		""" try add new age without admin logged in"""

		# add new age

		headers = {'token':''}
		data = {'minage':40, 'maxage':50}


		# post requset
		result = self.client_app.post("/api/addage", data=json.dumps(data), headers=headers,\
									content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')
		self.assertEqual(data['message'], "Invalid token. Please log in again.")
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 202)

