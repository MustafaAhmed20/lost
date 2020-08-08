from . import TestConfig
from app.api_views.user import *
from app.logic.operation import getCountry
import json
import os

# 'UserVerificationNumber' model
from app.models import UserVerificationNumber, Users

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

	def test_update(self):
		# update the user data

		# first log-in with admin
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

		# update the admin data - just the name
		token = data['data']['token']
		headers = {"token":token}

		data = {'name':"new name"}
		
		# put requset
		result = self.client_app.put("/api/modifyuser", data=json.dumps(data), headers=headers ,content_type='application/json')

		data = json.loads(result.data.decode())
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

		# check the new name in the database
		user = Users.query.filter_by(name='new name').first()

		self.assertTrue(user, "update admin name failed")
		self.assertEqual(user.phone, admin_phone, "admin phone don't match")

	def test_update2(self):
		# update the user data - update the password

		# first log-in with admin
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

		# update the admin data 
		token = data['data']['token']
		headers = {"token":token}

		data = {"password":admin_password, "newpassword": "newpassword123"}
		
		# put requset
		result = self.client_app.put("/api/modifyuser", data=json.dumps(data), headers=headers ,content_type='application/json')

		data = json.loads(result.data.decode())
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

		# check the new name in the database
		user = Users.query.filter_by(phone=admin_phone).first()

		self.assertTrue(user, "update admin name failed")
		self.assertEqual(user.phone, admin_phone, "admin phone don't match")

class TestUserApi3(TestConfig):
	""" tests the register user and confirm number"""

	def test_registerUser(self):
		''' regster user'''

		# the user country
		country = getCountry(phoneCode=249)

		data = {'phone':'+249929596047', 'password':'19823h', 'country_id':country.id, 'name':'mustafa'}
		
		# post requset
		result = self.client_app.post("/api/registeruser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

		# get sure the code get added to database
		#code = UserVerificationNumber.query.first()

		#self.assertTrue(code, 'no Verification Number')

	def test_registerUser2(self):
		''' regster user withot name'''

		# the user country
		country = getCountry(phoneCode=249)

		data = {'phone':'+249929596047', 'password':'19823h', 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/registeruser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

		# get sure the code get added to database
		#code = UserVerificationNumber.query.first()

		#self.assertTrue(code, 'no Verification Number')

	def test_registerUser3(self):
		''' regster user - invalid phone number'''

		# the user country
		country = getCountry(phoneCode=249)

		data = {'phone':'00929596047', 'password':'19823h', 'country_id':country.id, 'name':'mustafa'}
		
		# post requset
		result = self.client_app.post("/api/registeruser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'failure')
		self.assertEqual(data['message'], 'phone number not pass the validation')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)

	def test_registerUser4(self):
		''' regster user - invalid password'''

		# the user country
		country = getCountry(phoneCode=249)

		data = {'phone':'929596047', 'password':'123h', 'country_id':country.id, 'name':'mustafa'}
		
		# post requset
		result = self.client_app.post("/api/registeruser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'failure')
		self.assertEqual(data['message'], 'Password not pass the validation')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)

	def test_registerUser5(self):
		''' register User then conform it '''

		# the user country
		country = getCountry(phoneCode=249)

		data = {'phone':'+249929596047', 'password':'19823h', 'country_id':country.id, 'name':'mustafa'}
		
		# post requset
		result = self.client_app.post("/api/registeruser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

		# get sure the code get added to database
		# code = UserVerificationNumber.query.first()

		# self.assertTrue(code, 'no Verification Number')


		# # now conform the number

		# headers = {'token':data['data']['token']}
		# data = {'code':code.code}

		# # post requset
		# result = self.client_app.post("/api/conformuserphone", data=json.dumps(data),\
		# 		headers=headers, content_type='application/json')

		# data = json.loads(result.data.decode())

		# self.assertEqual(data['status'], 'success')
		# self.assertEqual(result.content_type,  'application/json')
		# self.assertEqual(result.status_code, 200)

class TestUserApi4(TestConfig):
	""" tests the forget password and rest password"""

	def test_forgotPassword(self):
		''' tests the forgotPassword route'''

		# the user country
		country = getCountry(phoneCode=20)
		admin_phone = os.getenv('admin_phone')

		data = {'phone':admin_phone, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/forgotpassword", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

		# test with not found user

		country = getCountry(phoneCode=249)
		
		data = {'phone':'929596047', 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/forgotpassword", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'failure')
		self.assertEqual(data['message'], 'no user with this phone')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 202)

	def test_resetPassword(self):
		''' test the 'resetPassword' route '''

		# first requset a code with the admon phone

		# the user country
		country = getCountry(phoneCode=20)
		admin_phone = os.getenv('admin_phone')

		data = {'phone':admin_phone, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/forgotpassword", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

		# get the code from the database

		code = UserVerificationNumber.query.first()

		# now check with the resetPassword route (withot the new password)

		data = {'phone':admin_phone, 'country_id':country.id, 'code':code.code}
		# post requset
		result = self.client_app.post("/api/resetpassword", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)


		# now check with the resetPassword route (with the new password)

		data = {'phone':admin_phone, 'country_id':country.id, 'code':code.code, 'password':'newpassword123'}
		
		# post requset
		result = self.client_app.post("/api/resetpassword", data=json.dumps(data), content_type='application/json')
		
		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)


		# now check agin - must failed becouse the code get deleted

		data = {'phone':admin_phone, 'country_id':country.id, 'code':code.code, 'password':'newpassword123'}
		# post requset
		result = self.client_app.post("/api/resetpassword", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		
		self.assertEqual(data['status'], 'failure')
		self.assertEqual(data['message'], 'Invalid code.')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 202)

	def test_getPermission(self):
		''' tests getpermission route'''

		result = self.client_app.get("/api/getpermission", content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertGreater(len(data['data']['permission']), 2, 'not right number of permission')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_getStatus(self):
		''' tests the getStatus route'''

		result = self.client_app.get("/api/getstatus", content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertGreater(len(data['data']['status']), 2, 'not right number of status')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_getuser(self):
		''' tests the 'getuser' route'''

		# get the user data with phone
		admin_phone = os.getenv('admin_phone')
		data = {'phone':admin_phone}

		result = self.client_app.post("/api/getuser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(len(data['data']['user']), 1, 'not right number of users')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)


		# get the user data with public id
		admin_phone = os.getenv('admin_phone')
		admin = getUser(phone=admin_phone)

		data = {'userid':admin.public_id}
		result = self.client_app.post("/api/getuser", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(len(data['data']['user']), 1, 'not right number of users')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)
