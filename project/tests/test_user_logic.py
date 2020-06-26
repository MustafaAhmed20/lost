""" tests the logic/user.py"""
from . import TestConfig
from app.logic.user import *

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

		self.assertTrue(user)
		self.assertEqual(result, True, 'add user Failed')

	def test_addUser2(self):
		'''add new user'''

		result = addUser(name='test', phone='1234567890', password=123, status='in_active')

		user = Users.query.filter_by(name='test').first()

		# the new user in inactive list
		inactive = Status.query.filter_by(name='in_active').first()

		self.assertIn(user, inactive.users)
		self.assertTrue(user)
		self.assertEqual(result, True, 'add user Failed')

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

		self.assertTrue(status)
		self.assertEqual(result, True, 'add status Failed')

	def test_addPermission(self):
		""" add new user permission """
		result = addPermission(name='super_user')

		permission = Permission.query.filter_by(name='super_user').first()

		self.assertTrue(permission)
		self.assertEqual(result, True, 'add permission Failed')

class TestUserLogic2(TestConfig):
	
	def test_getUser(self):
		""" add user the get it"""
		addUser(name='mustafa', phone=12345678, password=123)

		user = getUser(phone=12345678)


		self.assertTrue(user)
		self.assertEqual(user.name, 'mustafa', 'get user Failed')


