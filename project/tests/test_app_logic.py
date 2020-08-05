""" tests the logic/app.py"""
from . import TestConfig
from app.logic.app import *
from app.logic.user import getUser
from app.models import Feedback
import os


class TestAppLogic(TestConfig):

	def test_validatePhoneNumber(self):
		''' tests the "validate Phone Number" func '''

		countryCode = 249
		maxPhoneLength = 9

		# valid phones
		phone1 = '00249929596047'
		phone2 = '+249929596047'
		phone3 = '249929596047'
		phone4 = '929596047'
		phone5 = '0929596047'

		self.assertTrue(validatePhoneNumber(phone1, countryCode, maxPhoneLength), "phone1 did't pass the validation" )
		self.assertTrue(validatePhoneNumber(phone2, countryCode, maxPhoneLength), "phone2 did't pass the validation" )
		self.assertTrue(validatePhoneNumber(phone3, countryCode, maxPhoneLength), "phone3 did't pass the validation" )
		self.assertTrue(validatePhoneNumber(phone4, countryCode, maxPhoneLength), "phone4 did't pass the validation" )
		self.assertTrue(validatePhoneNumber(phone5, countryCode, maxPhoneLength), "phone5 did't pass the validation" )

	def test_validatePhoneNumber2(self):
		''' tests the "validate Phone Number" func not valid numbers'''

		countryCode = 249
		maxPhoneLength = 9

		# valid phons
		phone1 = '0249929596047'
		phone2 = '+24929596047'
		phone3 = '24992959604'
		phone4 = '9295960477'
		phone5 = '00929596047'
		
		
		self.assertFalse(validatePhoneNumber(phone1, countryCode, maxPhoneLength), "phone1 did't pass the validation" )
		self.assertFalse(validatePhoneNumber(phone2, countryCode, maxPhoneLength), "phone2 did't pass the validation" )
		self.assertFalse(validatePhoneNumber(phone3, countryCode, maxPhoneLength), "phone3 did't pass the validation" )
		self.assertFalse(validatePhoneNumber(phone4, countryCode, maxPhoneLength), "phone4 did't pass the validation" )
		self.assertFalse(validatePhoneNumber(phone5, countryCode, maxPhoneLength), "phone5 did't pass the validation" )

	def test_validatePassword(self):
		''' tests 'validatePassword' func '''

		# valid passwords
		pass1 = '1234A'
		pass2 = '12334s'
		pass3 = '12y34A'
		pass4 = '1234A%#'
		pass5 = '1234dGs'

		self.assertTrue(validatePassword(pass1, 5), "password 'pass1' did't pass the validation" )
		self.assertTrue(validatePassword(pass2, 5), "password 'pass2' did't pass the validation" )
		self.assertTrue(validatePassword(pass3, 5), "password 'pass3' did't pass the validation" )
		self.assertTrue(validatePassword(pass4, 5), "password 'pass4' did't pass the validation" )
		self.assertTrue(validatePassword(pass5, 5), "password 'pass5' did't pass the validation" )

	def test_validatePassword2(self):
		''' tests 'validatePassword' func with invalid passwords'''

		# valid passwords
		pass1 = '124A' # short
		pass2 = '1233423' # no letters
		pass3 = 'afknjf' # no numbers
		

		self.assertFalse(validatePassword(pass1, 5), "password 'pass1' pass the validation" )
		self.assertFalse(validatePassword(pass2, 5), "password 'pass2' pass the validation" )
		self.assertFalse(validatePassword(pass3, 5), "password 'pass3' pass the validation" )

class TestAppLogic2(TestConfig):
	""" tests the feedback logic"""

	def test_addFeedback(self):
		''' add feedback'''

		text = "this app is very awesome, thank you for your hard work"

		result = addFeedback(text=text)

		self.assertTrue(result)

		# check it in the database
		feedback = Feedback.query.all()

		self.assertEqual(len(feedback), 1, 'no feedback added')
		self.assertEqual(feedback[0].feedback, text, 'not the same feedback')

	def test_addFeedback2(self):
		''' add feedback, then get it'''

		# get admin id
		admin_phone = os.getenv('admin_phone')
		admin = getUser(phone=admin_phone)

		text = "this app is very awesome, thank you for your hard work"

		result = addFeedback(text=text, userPublicId=admin.public_id)

		self.assertTrue(result)

		# check it in the database
		feedback = Feedback.query.all()

		self.assertEqual(len(feedback), 1, 'no feedback added')
		self.assertEqual(feedback[0].feedback, text, 'not the same feedback')

		# check the feedback with the func
		feedback = getFeedback(userPublicId=admin.public_id)

		self.assertEqual(len(feedback), 1, 'no feedback added')
		self.assertEqual(feedback[0].feedback, text, 'not the same feedback')
		self.assertEqual(feedback[0].user_public_id, admin.public_id, 'not the same user')

	def test_addFeedback3(self):
		''' add feedback, then get it then delete it'''

		# get admin id
		admin_phone = os.getenv('admin_phone')
		admin = getUser(phone=admin_phone)

		text = "this app is very awesome, thank you for your hard work"

		result = addFeedback(text=text, userPublicId=admin.public_id)

		self.assertTrue(result)

		# check it in the database
		feedback = Feedback.query.all()

		self.assertEqual(len(feedback), 1, 'no feedback added')
		self.assertEqual(feedback[0].feedback, text, 'not the same feedback')

		# check the feedback with the func
		feedback = getFeedback(userPublicId=admin.public_id)

		self.assertEqual(len(feedback), 1, 'no feedback added')
		self.assertEqual(feedback[0].feedback, text, 'not the same feedback')
		self.assertEqual(feedback[0].user_public_id, admin.public_id, 'not the same user')

		# now delete the feedback
		result = deleteFeedback(userPublicId=admin.public_id)

		self.assertTrue(result)

		# must be empty feedback now
		feedback = getFeedback()

		self.assertFalse(feedback)
		self.assertEqual(len(feedback), 0)

		
		# add new one and delete it by id
		result = addFeedback(text=text)

		self.assertTrue(result)

		# check it in the database
		feedback = Feedback.query.all()

		self.assertEqual(len(feedback), 1, 'no feedback added')
		self.assertEqual(feedback[0].feedback, text, 'not the same feedback')

		# now delete the feedback
		result = deleteFeedback(id=feedback[0].id)

		self.assertTrue(result)

		# must be empty feedback now
		feedback = getFeedback()

		self.assertFalse(feedback)
		self.assertEqual(len(feedback), 0)


	