""" tests the logic/user.py"""
from . import TestConfig
from app.logic.user import *
from app.models import Status, UserVerificationNumber

import os

class TestUserLogic(TestConfig):
	""" tests the User model operations """
	def test_login(self):
		"""login with default admin"""
		result = login(userPhone=os.getenv('admin_phone'), userPassword=os.getenv('admin_pass'))

		self.assertEqual(result, True, 'admin login Failed')

	def test_login2(self):
		"""login with default admin"""
		
		result = login(userPhone=os.getenv('admin_phone')+'0', userPassword=os.getenv('admin_pass'))

		self.assertNotEqual(result, True, 'login worked when should not')

	def test_addUser(self):
		'''add new user'''

		result = addUser(name='test', phone='1234567890', password=123)

		user = Users.query.filter_by(name='test').first()

		self.assertTrue(user, 'add user Failed')
		self.assertEqual(result.name, 'test', 'add user Failed')

	def test_addUser2(self):
		'''add new user'''

		result = addUser(name='test', phone='1234567890', password=123, status='in_active')

		user = Users.query.filter_by(name='test').first()

		# the new user in inactive list
		inactive = Status.query.filter_by(name='in_active').first()

		self.assertIn(user, inactive.users)
		self.assertTrue(user)
		self.assertEqual(result.name, 'test', 'add user Failed')

	def test_toAdmin(self):
		""" add user then promote to admin"""
		addUser(name='test', phone='1234567890', password=123)

		user = Users.query.filter_by(name='test').first()
		
		result = changeUserPermission(user.public_id, 'admin')

		# the new user in admins list
		admin = Permission.query.filter_by(name='admin').first()

		self.assertIn(user, admin.users, 'the new user not an admin')

		self.assertEqual(result, True, 'promote to admin Failed')

	def test_toManager(self):
		""" add user then promote to manager"""
		addUser(name='test', phone='1234567890', password=123)

		user = Users.query.filter_by(name='test').first()
		
		result = changeUserPermission(user.public_id, 'manager')

		# the new user in admins list
		manager = Permission.query.filter_by(name='manager').first()

		self.assertIn(user, manager.users, 'the new user not an manager')

		self.assertEqual(result, True, 'promote to manager Failed')

	def test_toInactive(self):
		""" add user then change stataus to inactive"""
		addUser(name='test', phone='1234567890', password=123)

		user = Users.query.filter_by(name='test').first()
		
		result = changeUserStatus(user.public_id, 'in_active')

		# the new user in inactive list
		inactive = Status.query.filter_by(name='in_active').first()

		self.assertIn(user, inactive.users, 'the new user not an inactive')

		self.assertEqual(result, True, 'change to inactive Failed')

	def test_addStatus(self):
		""" add new user status """
		result = addStatus(name='deleted')

		status = Status.query.filter_by(name='deleted').first()

		self.assertTrue(status, 'add status Failed')
		self.assertEqual(result.name, 'deleted', 'add status Failed')

	def test_addPermission(self):
		""" add new user permission """
		result = addPermission(name='super_user')

		permission = Permission.query.filter_by(name='super_user').first()

		self.assertTrue(permission, 'add permission Failed')
		self.assertEqual(result.name, 'super_user', 'add permission Failed')

class TestUserLogic2(TestConfig):
	
	def test_getUser(self):
		""" add user the get it"""
		addUser(name='mustafa', phone=12345678, password=123)

		user = getUser(phone=12345678)


		self.assertTrue(user)
		self.assertEqual(user.name, 'mustafa', 'get user Failed')

		# get the user with public id

		public_id = user.public_id
		user = getUser(publicId=public_id)

		self.assertTrue(user)
		self.assertEqual(user.name, 'mustafa', 'get user Failed')
		self.assertEqual(user.public_id, public_id, 'not same public Id')

	def test_registerUser(self):
		''' regster a user and get the Verification code'''

		result = registerUser(name='mustafa', phone=12345678, password=123)

		# success register
		self.assertTrue(result)

		user, code = result

		self.assertEqual(user.name, 'mustafa', 'get user Failed')
		#self.assertEqual(code.user_id, user.id, 'create code Failed')

		# valid code
		#self.assertTrue(code.code)
		#self.assertEqual(len(code.code), 6, 'create code length Failed')
		
	def test_registerUser2(self):
		''' register a User then confirm the number '''

		# first register the user
		result = registerUser(name='mustafa', phone=12345678, password=123)

		# success register
		self.assertTrue(result)

		user, code = result

		self.assertEqual(user.name, 'mustafa', 'get user Failed')
		#self.assertEqual(code.user_id, user.id, 'create code Failed')

		# valid code
		#self.assertTrue(code.code)
		#self.assertEqual(len(code.code), 6, 'create code length Failed')

		# Verify the user

		#result = VerifyUser(user_id=user.id, code=code.code)

		# success Verification
		#self.assertTrue(result)

		# make sure the user is active now
		active = Status.query.filter_by(name='active').first()

		self.assertIn(user, active.users)

	def test_registerUser3(self):
		''' register a User(without name)then confirm the number '''

		# first register the user
		result = registerUser(phone=12345678, password=123)

		# success register
		self.assertTrue(result)

		user, code = result

		self.assertEqual(user.phone, '12345678', 'get user Failed')
		#self.assertEqual(code.user_id, user.id, 'create code Failed')

		# valid code
		#self.assertTrue(code.code)
		#self.assertEqual(len(code.code), 6, 'create code length Failed')

		# Verify the user

		#result = VerifyUser(user_id=user.id, code=code.code)

		# success Verification
		#self.assertTrue(result)

		# make sure the user is active now
		active = Status.query.filter_by(name='active').first()

		self.assertIn(user, active.users)

	def test_forgotPassword(self):
		''' tests the 'forgotPassword' func'''

		admin_phone = os.getenv('admin_phone')
		admin = getUser(phone=os.getenv('admin_phone'))

		result = forgotPassword(admin_phone)

		self.assertTrue(result)

		self.assertEqual(result.user_id, admin.id)

		# try with not found user

		result = forgotPassword('929596047')

		self.assertFalse(result)

		# try add a new code to same user - should delete the first automatically

		result = forgotPassword(admin_phone)

		self.assertTrue(result)
		self.assertEqual(result.user_id, admin.id)

		# one code
		codes = UserVerificationNumber.query.all()

		self.assertEqual(len(codes), 1)

	def test_resetPassword(self):
		''' tests the 'resetPassword' func '''

		# first add a code to admin
		admin_phone = os.getenv('admin_phone')
		admin = getUser(phone=os.getenv('admin_phone'))

		resultCode = forgotPassword(admin_phone)

		self.assertTrue(resultCode)

		# now just check if the code is correct
		result = resetPassword(resultCode.code, admin_phone, newPassword=None)

		self.assertTrue(result)

		# now check and reset the password
		result = resetPassword(resultCode.code, admin_phone, newPassword='thisnewpassword')

		self.assertTrue(result)

		# try again - must fails becous the code deleted
		result = resetPassword(resultCode.code, admin_phone, newPassword='thisnewpassword')

		self.assertFalse(result)

class TestUserLogic3(TestConfig):
	""" tests the user logic"""

	def test_getStatus(self):

		status = getStatus(name='active')

		self.assertTrue(status, 'no status returned')

		status = getStatus()
		self.assertTrue(status, 'no status returned')
		self.assertGreater(len(status), 2, 'not right number of status')

	def test_getPermission(self):

		permission = getPermission(name='user')

		self.assertTrue(permission, 'no Permission returned')

		permission = getPermission()
		self.assertTrue(permission, 'no Permission returned')
		self.assertGreater(len(permission), 2, 'not right number of permission')

class TestUserHelperFunctions(TestConfig):

	def test_createVerifyCode(self):
		''' test the create code func'''
		from app.logic.user import _createVerifyCode


		code = _createVerifyCode()

		self.assertTrue(code, 'no code generated')
		self.assertEqual(len(code), 6, 'the code length is not right')

	def test_restPassword(self):
		''' tests the rest Password func '''
		from app.logic.user import _restPassword

		admin = getUser(phone=os.getenv('admin_phone'))

		# change the password
		result = _restPassword(admin.id, 'thisnewpassword')

		self.assertTrue(result)

		# try login with the new password
		result = login(os.getenv('admin_phone'), 'thisnewpassword')

		self.assertTrue(result)

	def test_deleteUserCode(self):
		''' delete the code for admin'''
		from app.logic.user import _deleteUserCode

		admin_phone = os.getenv('admin_phone')
		admin = getUser(phone=os.getenv('admin_phone'))

		# first create code for admin
		result = forgotPassword(admin_phone)

		self.assertTrue(result)

		# now dlete the code
		result = _deleteUserCode(admin.id)

		self.assertTrue(result)

		# now check if it deleted
		codes = UserVerificationNumber.query.all()
		self.assertFalse(codes)

	def test_createPublicId(self):
		''' tests 'createPublicId' func '''
		from app.logic.user import _createPublicId

		publicId = _createPublicId()

		self.assertTrue(publicId, 'no public Id returned')
		self.assertGreater(len(publicId), 30, 'wrong length of public Id')

