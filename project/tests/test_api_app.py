from . import TestConfig
from app.api_views.app import *
from app.models import Feedback
from app.logic.operation import getCountry
from app.logic.user import getUser

import json
import os


class TestAppApi(TestConfig):

	def test_checkconnection(self):
		''' test the 'check connection' route'''
		result = self.client_app.get("/api/checkconnection", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

class TestAppApi2(TestConfig):
	""" tests the feedback Routes"""

	def test_addfeedback(self):
		''' add feedbak without login'''

		text = "this app is very awesome, thank you for your hard work"

		data = {"feedback":text}

		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)

		# check the feedback in the database
		feedback = Feedback.query.all()

		self.assertTrue(feedback, 'no feedback added')
		self.assertEqual(len(feedback), 1, "wrong length of feedback numbers")

	def test_addfeedback2(self):
		''' add feedbak with logined user'''

		# login with admin
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		# the user country
		country = getCountry(phoneCode=20)

		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		# get the token
		token = data['data']['token']
		headers = {'token':token}


		text = "this app is very awesome, thank you for your hard work"

		data = {"feedback":text}

		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), 
									headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)

		# check the feedback in the database
		feedback = Feedback.query.all()

		self.assertTrue(feedback, 'no feedback added')
		self.assertEqual(len(feedback), 1, "wrong length of feedback numbers")

		# check admin id
		self.assertTrue(feedback[0].user_public_id, "no user id added")

	def test_getfeedback(self):
		''' tests the getfeedback Route'''

		# first add feedback

		text = "this app is very awesome, thank you for your hard work"

		data = {"feedback":text}

		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)

		# now get it

		# first login with admin
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
	
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		# get the token
		token = data['data']['token']
		headers = {'token':token}


		result = self.client_app.post("/api/getfeedback",  data=json.dumps({}), headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(len(data['data']['feedback']), 1)
		self.assertEqual(result.status_code, 200)

	def test_getfeedback2(self):
		''' tests the getfeedback Route (with user id)'''

		# login with admin
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		# the user country
		country = getCountry(phoneCode=20)

		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		# get the token
		token = data['data']['token']
		headers = {'token':token}


		text = "this app is very awesome, thank you for your hard work"

		data = {"feedback":text}

		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), 
									headers=headers, content_type='application/json')

		# now get the feedback with the route

		# get the public id of the admin
		admin = getUser(phone=admin_phone)

		data = {'userid':admin.public_id}
		result = self.client_app.post("/api/getfeedback", data=json.dumps(data), 
									headers=headers,content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(len(data['data']['feedback']), 1)
		self.assertEqual(result.status_code, 200)

	def test_deletefeedback(self):
		''' tests the deletefeedback route'''

		# add first
		text = "this app is very awesome, thank you for your hard work"

		data = {"feedback":text}

		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)

		# check the feedback in the database
		feedback = Feedback.query.all()

		self.assertTrue(feedback, 'no feedback added')
		self.assertEqual(len(feedback), 1, "wrong length of feedback numbers")

		# login as admin

		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		# the user country
		country = getCountry(phoneCode=20)

		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		# get the token
		token = data['data']['token']
		headers = {'token':token}

		# get the feedback id
		result = self.client_app.post("/api/getfeedback",  data=json.dumps({}), headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())

		feedbackId = data['data']['feedback'][0]['id']

		# delete the feedback
		data ={'feedbackid':feedbackId}
		result = self.client_app.delete("/api/deletefeedback",  data=json.dumps(data), headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		# now check if its deleted
		result = self.client_app.post("/api/getfeedback",  data=json.dumps({}), headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(len(data['data']['feedback']), 0)
		self.assertEqual(result.status_code, 200)

	def test_deletefeedback2(self):
		''' delete feedback with user id'''

		# login with admin
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		# the user country
		country = getCountry(phoneCode=20)

		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		# get the token
		token = data['data']['token']
		headers = {'token':token}


		text = "this app is very awesome, thank you for your hard work"

		data = {"feedback":text}

		# add three feddbacks with admin

		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), 
									headers=headers, content_type='application/json')
		
		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), 
									headers=headers, content_type='application/json')
		
		result = self.client_app.post("/api/addfeedback", data=json.dumps(data), 
									headers=headers, content_type='application/json')

		# make sure the feedback get added
		feedback = Feedback.query.all()
		self.assertEqual(len(feedback), 3, 'not rigth numbers of feedback')

		# get the admin public id
		admin = getUser(phone=admin_phone)

		# delete with admin id

		data = {'userid':admin.public_id}
		
		result = self.client_app.delete("/api/deletefeedback",  data=json.dumps(data), headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		# now check if its deleted
		result = self.client_app.post("/api/getfeedback",  data=json.dumps({}), headers=headers, content_type='application/json')

		data = json.loads(result.data.decode())
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(len(data['data']['feedback']), 0)
		self.assertEqual(result.status_code, 200)

