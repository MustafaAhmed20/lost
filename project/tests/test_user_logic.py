""" tests the logic/user.py"""
from . import TestConfig
from app.logic.user import *
from app.models.user import Users

import os

class TestUserLogic(TestConfig):
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

		self.assertEqual(result, True, 'add user Failed')

	def test_toAdmin(self):
		""" add user the promote to admin"""
		addUser(name='test', phone='1234567890', password=123)

		user = Users.query.filter_by(name='test').first()
		
		result = changeUserPermission(user.public_id, 'admin')

		self.assertEqual(result, True, 'promote to admin Failed')