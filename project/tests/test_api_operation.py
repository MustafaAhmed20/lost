from . import TestConfig
from app.api_views.operation import *
from app.logic.operation import getCountry
from app.logic.person import getPerson, getPohto

import json
import os
from io import BytesIO

class TestOperationApi(TestConfig):

	def test_addcountry(self):
		# first login as admin
		
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')
		
		data = {'phone':admin_phone, 'password':admin_password}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		adminToken = data['data']['token']

		# add new country
		headers = {'token':adminToken}
		data = {'name': 'usa', 'phone_code':1}

		result = self.client_app.post("/api/addcountry", data=json.dumps(data),\
									 headers=headers,content_type='application/json')

		
		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')		
		self.assertEqual(data['message'],  None)
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 201)

		
		country = getCountry(name='usa')
		self.assertTrue(country, 'no country')
		self.assertEqual(country.name, 'usa', 'no country')
		self.assertEqual(country.phone_code, 1, 'no country')

	def test_addcountry2(self):
		""" try add country without valid data"""
		# first login as admin
		
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')
		
		if not admin_phone or not admin_password:
			raise ValueError('Environment variables not found!')
		
		data = {'phone':admin_phone, 'password':admin_password}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		adminToken = data['data']['token']

		# add new country
		headers = {'token':adminToken}
		data = {}

		result = self.client_app.post("/api/addcountry", data=json.dumps(data),\
									 headers=headers,content_type='application/json')

		
		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')		
		self.assertEqual(data['message'],  'required data not submitted')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)

		
		data = {'name': 'usa'}

		result = self.client_app.post("/api/addcountry", data=json.dumps(data),\
									 headers=headers,content_type='application/json')

		
		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')		
		self.assertEqual(data['message'],  'required data not submitted')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)	


		# already exists
		
		data = {'name': 'sudan', 'phone_code':249}

		result = self.client_app.post("/api/addcountry", data=json.dumps(data),\
									 headers=headers,content_type='application/json')


		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')		
		self.assertEqual(data['message'],  'Country already exists.')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 202)

		
	def test_getcountry(self):
		""" test the /getcountry route"""

		result = self.client_app.get("/api/getcountry", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['country'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_getcountry2(self):
		""" test the /getcountry route with perm"""

		result = self.client_app.get("/api/getcountry/1", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['country'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)


	def test_getstatusoperation(self):
		""" test the /getstatusoperation route"""

		result = self.client_app.get("/api/getstatusoperation", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['status_operation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_getstatusoperation2(self):
		""" test the /getstatusoperation route with perm"""

		result = self.client_app.get("/api/getstatusoperation/1", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['status_operation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	
	def test_gettypeoperation(self):
		""" test the /gettypeoperation route"""

		result = self.client_app.get("/api/gettypeoperation", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['type_operation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_gettypeoperation2(self):
		""" test the /gettypeoperation route with perm"""

		result = self.client_app.get("/api/gettypeoperation/1", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['type_operation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)


class TestOperationApi2(TestConfig):

	def test_addoperation(self):
		""" add new operation"""

		# first log-in
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		data = {'phone':admin_phone, 'password':admin_password}
	
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())
		
		token = data['data']['token']

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		# add new operation
		headers = {'token':token}
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.getenv('IMEGE_TEST_NAME'))
		
		
		# send 3 photos
		photos = []
		for _ in range(3):
			photos.append((open(file_path, 'rb'), os.getenv('IMEGE_TEST_NAME')))
		
		
		
		data = {'photos':photos, 'date':'2020-11-15',
				'type_id':2, 'country_id':1,
				'object_type':'Person', 'person_name':'mustafa'}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		
		# close the files
		for file in photos:
			file[0].close()
		
		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)

		# the person get added
		person = getPerson()

		self.assertTrue(person)

		photos = getPohto()

		self.assertTrue(photos)
		self.assertEqual(len(photos), 3)

	def test_getoperation(self):
		""" add operations then get it """

		# first log-in 
		admin_phone = os.getenv('admin_phone')
		admin_password = os.getenv('admin_pass')

		data = {'phone':admin_phone, 'password':admin_password}
	
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())
		
		token = data['data']['token']

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		# add new operation
		headers = {'token':token}

		data = {'date':'2020-11-15',
				'type_id':1, 'country_id':'1',
				'object_type':'Person', 'person_name':'mustafa'}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)

		# add new operation2
		headers = {'token':token}

		data = {'date':'2020-10-25',
				'type_id':2, 'country_id':'2',
				'object_type':'Person', 'person_name':'test'}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)


		# get the operation
		data = {}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 2)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

		# get the operation wuth country id filter
		data = {'country_id':1}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 1)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

		# get the operation wuth country id filter
		data = {'type_id':2}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 1)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)


