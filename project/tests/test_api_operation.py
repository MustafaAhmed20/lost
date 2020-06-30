from . import TestConfig
from app.api_views.operation import *
import json
import os

class TestOperationApi(TestConfig):

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
		self.assertTrue(data['data']['statusoperation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_getstatusoperation2(self):
		""" test the /getstatusoperation route with perm"""

		result = self.client_app.get("/api/getstatusoperation/1", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['statusoperation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	
	def test_gettypeoperation(self):
		""" test the /gettypeoperation route"""

		result = self.client_app.get("/api/gettypeoperation", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['typeoperation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)

	def test_gettypeoperation2(self):
		""" test the /gettypeoperation route with perm"""

		result = self.client_app.get("/api/gettypeoperation/1", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertTrue(data['data']['typeoperation'])
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)
