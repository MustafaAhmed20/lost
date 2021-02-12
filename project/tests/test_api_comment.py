from . import TestConfig
from app.logic.operation import getCountry
import json, os

class TestCommentApi(TestConfig):

	def test_addcomment(self):
		''' test add comments on operation '''

		# first add the operation
		#

		# first log-in 
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
	
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())
		

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		token = data['data']['token']

		from app.models import Age
		age = Age.query.first()


		# add new operation
		headers = {'token':token}

		data = {'date':'2020-11-15',
				'type_id':1, 'country_id':'1',
				'object_type':'Person', 'person_name':'mustafa', 'gender':'male','age_id':age.id}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)

		
		# get the operation data
		#

		data = {}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 1)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)


		# the operation id
		operationId = data['data']['operations'][0]['id']


		# now add the comment
		#

		data = {'operationid':operationId, 'text':'this is the message body'}
		result = self.client_app.post("/api/sendcomment", data=json.dumps(data), headers=headers,\
			content_type="application/json")

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)

		
		# now get the comments
		#
		data = {'operationid':operationId}
		result=self.client_app.get('/api/getcomment', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['comments']), 1)
		self.assertEqual(data['data']['comments'][0]['text'],  'this is the message body')
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

