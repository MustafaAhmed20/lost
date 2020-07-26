from . import TestConfig
from app.api_views.user import *
from app.logic.operation import getCountry
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
		
		# the user country
		country = getCountry(phoneCode=20)

		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
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

		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':'wrong', 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')

		self.assertTrue(data['message'], 'wrong phone or password')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 202)

	def test_login3(self):
		""" test the login route without parameters"""
		
		data = {}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')

		self.assertEqual(data['message'], 'required data not submitted')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)

class TestUserApi2(TestConfig):
	""" tests the add user """

	def test_addUser(self):
		""" login with admin then add user"""

		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')

		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		resultAdmin = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(resultAdmin.data.decode())

		self.assertEqual(data['status'], 'success')

		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(resultAdmin.content_type,  'application/json')
		self.assertEqual(resultAdmin.status_code, 200)

		# add user

		# the user country
		country = getCountry(phoneCode=249)

		userData = {'name':'mustafa', 'phone':'0123456789', 'password':'12334a',\
					 'status':'active', 'permission':'user', 'country_id':country.id}

		headers = {'token':data['data']['token']}
		result = self.client_app.post("/api/adduser", data=json.dumps(userData),\
									 headers=headers,content_type='application/json')

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['status'], 'success')		
		self.assertEqual(data['message'],  None)
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

	def test_addUser2(self):
		""" login with admin then add user , then try add user with normal user"""

		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')
		
		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		resultAdmin = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(resultAdmin.data.decode())

		self.assertEqual(data['status'], 'success')

		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(resultAdmin.content_type,  'application/json')
		self.assertEqual(resultAdmin.status_code, 200)

		# add user

		# the user country
		country = getCountry(phoneCode=249)

		userData = {'name':'mustafa', 'phone':'0123456789', 'password':'12334a',\
					 'status':'active', 'permission':'user', 'country_id':country.id}

		headers = {'token':data['data']['token']}
		result = self.client_app.post("/api/adduser", data=json.dumps(userData),\
									 headers=headers,content_type='application/json')

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['status'], 'success')		
		self.assertEqual(data['message'],  None)
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)
		

		# try add user with the new user

		# login
		normalUserData = {'phone':'0123456789', 'password':'12334a', 'country_id':country.id}
		noremalUserResult = self.client_app.post("/api/login", data=json.dumps(normalUserData), content_type='application/json')

		normalUser = json.loads(noremalUserResult.data.decode())

		normalUserToken = normalUser['data']['token']


		self.assertEqual(normalUser['status'], 'success')
		self.assertTrue(normalUserToken, 'no token returned')
		self.assertEqual(noremalUserResult.content_type,  'application/json')
		self.assertEqual(noremalUserResult.status_code, 200)

		# add user
		
		testUserData = {'name':'test', 'phone':'0123456789', 'password':'123es2',\
					 'status':'active', 'permission':'user'}

		headers = {'token': normalUserToken}
		result = self.client_app.post("/api/adduser", data=json.dumps(testUserData),\
									 headers=headers,content_type='application/json')

		testData = json.loads(result.data.decode())

		self.assertEqual(testData['status'], 'failure')
		self.assertEqual(testData['message'], "You don't have the permission.")
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 401)
	
	def test_addUser3(self):
		""" login with admin then add user withot the defulat values"""

		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')
		
		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		resultAdmin = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(resultAdmin.data.decode())

		self.assertEqual(data['status'], 'success')

		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(resultAdmin.content_type,  'application/json')
		self.assertEqual(resultAdmin.status_code, 200)

		# add user

		# the user country
		country = getCountry(phoneCode=249)

		userData = {'name':'mustafa', 'phone':'0123456789', 'password':'12334a',\
					 'status':'active', 'permission':'user', 'country_id':country.id}

		headers = {'token':data['data']['token']}
		result = self.client_app.post("/api/adduser", data=json.dumps(userData),\
									 headers=headers,content_type='application/json')

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['status'], 'success')		
		self.assertEqual(data['message'],  None)
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

	def test_addUser4(self):
		""" login with admin then add user then try add same user again"""

		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')
		
		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		resultAdmin = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(resultAdmin.data.decode())

		self.assertEqual(data['status'], 'success')

		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(resultAdmin.content_type,  'application/json')
		self.assertEqual(resultAdmin.status_code, 200)

		# add user

		# the user country
		country = getCountry(phoneCode=249)

		userData = {'name':'mustafa', 'phone':'0123456789', 'password':'12334a',\
					 'status':'active', 'permission':'user', 'country_id':country.id}

		headers = {'token':data['data']['token']}
		result = self.client_app.post("/api/adduser", data=json.dumps(userData),\
									 headers=headers,content_type='application/json')

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['status'], 'success')		
		self.assertEqual(data['message'],  None)
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

		# add same user

		result = self.client_app.post("/api/adduser", data=json.dumps(userData),\
									 headers=headers,content_type='application/json')

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['status'], 'failure')		
		self.assertEqual(data['message'],'User already exists. Please Log in.')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 202)

