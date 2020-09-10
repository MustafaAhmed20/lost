from . import TestConfig
from app.api_views.operation import *
from app.logic.operation import getCountry
from app.logic.person import getPerson, getPohto, deletePerson


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
		
		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
		
		# post requset
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		adminToken = data['data']['token']

		# add new country
		headers = {'token':adminToken}
		data = {'name': 'usa', 'phone_code':1, 'phone_length':10, 'iso_name':'USA'}

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
		self.assertEqual(country.iso_name, 'USA', 'no country')

	def test_addcountry2(self):
		""" try add country without valid data"""
		# first login as admin
		
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

		
		data = {'name': 'usa', 'phone_length':10}

		result = self.client_app.post("/api/addcountry", data=json.dumps(data),\
									 headers=headers,content_type='application/json')

		
		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'failure')		
		self.assertEqual(data['message'],  'required data not submitted')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 400)	


		# already exists
		
		data = {'name': 'sudan', 'phone_code':249, 'phone_length':9, 'iso_name':'SD'}

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

		# the user country
		country = getCountry(phoneCode=20)
		
		data = {'phone':admin_phone, 'password':admin_password, 'country_id':country.id}
	
		result = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(result.data.decode())
		

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 200)

		token = data['data']['token']


		# add new operation
		headers = {'token':token}
		file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.getenv('IMEGE_TEST_NAME'))


		# send 3 photos
		photos = []
		for _ in range(3):
			photos.append((open(file_path, 'rb'), os.getenv('IMEGE_TEST_NAME')))

		from app.models import Age
		age = Age.query.first()



		data = {'photos':photos, 'date':'2020-11-15',
				'type_id':2, 'country_id':1,
				'object_type':'Person', 'person_name':'mustafa', 'gender':'male', 'age_id':age.id}

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

		self.assertTrue(person[0])

		photos = getPohto(object=person[0])

		self.assertTrue(photos)
		self.assertEqual(len(photos), 3)

		# delete person to get rid of the photos
		deletePerson(id=person[0].id)

		# no photos after delete
		self.assertEqual(len(getPohto()), 0, 'photos not deleted')

	def test_addoperation2(self):
		""" add operations then get it """

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

		# add new operation2
		headers = {'token':token}

		data = {'date':'2020-10-25',
				'type_id':2, 'country_id':'2',
				'object_type':'Car', "brand":'brand', "model":'model', 
				"plate_number_letters":"klj", "plate_number_numbers":"123",
				"car_type": "1"}

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

		# get the operation with object=Peron filter
		data = {'object':"Person"}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 1)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

		# get the operation with object=Car filter
		data = {'object':"Car"}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 1)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)


		# get the operation with wrong object filter
		data = {'object':"wrong"}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 0)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

		# get the operation with not exist data
		data = {'id':"4"}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())

		self.assertTrue(data, 'no operations')
		self.assertEqual(len(data['data']['operations']), 0)
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

	def test_addoperation3(self):
		''' add operation with full data then get it '''

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


		# add new operation
		headers = {'token':token}

		lat = 48.856613
		lng = 2.352222

		from app.models import Age
		age = Age.query.first()

		data = {'date':'2020-11-15',
				'type_id':1, 'country_id':'1',
				'object_type':'Person', 'person_name':'mustafa', 'age_id':age.id,
				'details': 'this long paragraph of details', 'gender':'male', 'skin':2,
				'lat':lat, 'lng':lng}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())

		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)


		# get the operation
		data = {}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())


		self.assertTrue(data['data']['operations'])
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')

		self.assertEqual(data['data']['operations'][0]['details'], 'this long paragraph of details', 'no details')
		self.assertEqual(data['data']['operations'][0]['lat'], lat, 'no lat')
		self.assertEqual(data['data']['operations'][0]['lng'], lng, 'no lng')
		self.assertEqual(data['data']['operations'][0]['object']['skin'], 2, 'no skin')
		self.assertEqual(data['data']['operations'][0]['object']['age_id'], age.id, 'not same age')
		self.assertEqual(data['data']['operations'][0]['user']['name'], 'admin', 'no user')
		

		
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

	def test_addoperation4(self):
		''' add new user then add operation with it'''

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
		
		self.assertEqual(result.status_code, 201)

		# login with the new user
		data = {'phone':'0123456789', 'password':'12334a', 'country_id':country.id}
		resultAdmin = self.client_app.post("/api/login", data=json.dumps(data), content_type='application/json')

		data = json.loads(resultAdmin.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['token'], 'no token returned')
		self.assertEqual(resultAdmin.status_code, 200)

		token = data['data']['token']
		from app.models import Age
		age = Age.query.first()

		# try add operation with this user
		headers = {'token':token}

		data = {'date':'2020-11-15',
				'type_id':2, 'country_id':1,
				'object_type':'Person', 'person_name':'mustafa', 'gender':'male', 'age_id':age.id}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")
		
		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)

	def test_addoperation5(self):
		''' add operation with full data then get it - with 'car' object'''

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


		# add new operation
		headers = {'token':token}

		lat = 48.856613
		lng = 2.352222

		data = {'date':'2020-11-15',
				'type_id':1, 'country_id':'1',
				'object_type':'Car', 'model':'toyota', 'car_type':'1', 'brand':'brand',
				'plate_number_letters':'fds', 'plate_number_numbers': '321',
				'details': 'this long paragraph of details',
				'lat':lat, 'lng':lng}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())

		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)


		# get the operation
		data = {}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())


		self.assertTrue(data['data']['operations'])
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')

		self.assertEqual(data['data']['operations'][0]['details'], 'this long paragraph of details', 'no details')
		self.assertEqual(data['data']['operations'][0]['lat'], lat, 'no lat')
		self.assertEqual(data['data']['operations'][0]['lng'], lng, 'no lng')
		self.assertEqual(data['data']['operations'][0]['object']['model'], 'toyota', 'no car model')
		self.assertEqual(data['data']['operations'][0]['object']['brand'], 'brand', 'not same brand')
		self.assertEqual(data['data']['operations'][0]['user']['name'], 'admin', 'no user')
		

		
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)

	def test_addoperation6(self):
		''' add operation with full data then get it - with 'car' object'''

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


		# add new operation
		headers = {'token':token}

		lat = 48.856613
		lng = 2.352222

		data = {'date':'2020-11-15',
				'type_id':1, 'country_id':'1',
				'object_type':'Car', 'model':'toyota', 'car_type':'1', 'brand':'brand',
				'plate_number_letters':'fds', 'plate_number_numbers': '321',
				'details': 'this long paragraph of details',
				'lat':lat, 'lng':lng,
				'city':'giza', 'state':'cairo'}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())

		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.status_code, 201)


		# get the operation
		data = {}

		result=self.client_app.get('/api/getoperation', query_string=data, content_type='application/json')
		data = json.loads(result.data.decode())


		self.assertTrue(data['data']['operations'])
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')

		self.assertEqual(data['data']['operations'][0]['details'], 'this long paragraph of details', 'no details')
		self.assertEqual(data['data']['operations'][0]['lat'], lat, 'no lat')
		self.assertEqual(data['data']['operations'][0]['lng'], lng, 'no lng')
		self.assertEqual(data['data']['operations'][0]['city'], 'giza', 'not the same city')
		self.assertEqual(data['data']['operations'][0]['state'], 'cairo', 'not the same stete')
		self.assertEqual(data['data']['operations'][0]['object']['model'], 'toyota', 'no car model')
		self.assertEqual(data['data']['operations'][0]['object']['brand'], 'brand', 'not same brand')
		self.assertEqual(data['data']['operations'][0]['user']['name'], 'admin', 'no user')
		

		
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)
	"""
	def test_addoperation7(self):
		''' try add arabic data for the operation'''

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
				'object_type':'Person', 'person_name':'مصطفى', 'gender':'male','age_id':age.id}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)
	"""

class TestOperationApi3(TestConfig):
	
	def test_updateoperationStatus(self):
		''' tests the update operation status route'''

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
				'type_id':2, 'country_id':1,
				'object_type':'Person', 'person_name':'mustafa', 'gender':'male', 'age_id':age.id}

		result = self.client_app.post("/api/addoperation", data=data, headers=headers,\
			content_type="multipart/form-data")

		
		data = json.loads(result.data.decode())
		
		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 201)

		result = self.client_app.get("/api/getoperation", data=data,
			content_type="multipart/form-data")
		

		data = json.loads(result.data.decode())

		operation = data['data']['operations'][0]

		
		# now update status to closed
		data = {'status':'closed', 'operationid':operation['id']}

		result = self.client_app.put("/api/updateoperationstatus", data=data, headers=headers,\
			content_type="multipart/form-data")

		
		data = json.loads(result.data.decode())

		self.assertEqual(data['message'],  None)
		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type, 'application/json')
		self.assertEqual(result.status_code, 200)
