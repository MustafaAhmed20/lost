from . import TestConfig
from app.api_views.app import *

import json



class TestAppApi(TestConfig):

	def test_checkconnection(self):
		''' test the 'check connection' route'''
		result = self.client_app.get("/api/checkconnection", content_type='application/json')

		data = json.loads(result.data.decode())

		self.assertEqual(data['status'], 'success')
		self.assertEqual(result.content_type,  'application/json')
		self.assertEqual(result.status_code, 200)