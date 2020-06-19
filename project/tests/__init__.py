from app import create_app

from app.models import db

import unittest
import os


app = create_app()
app.app_context().push()

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI_testing')

app = app.test_client()

# raise error if no environment variable
assert os.getenv('SQLALCHEMY_DATABASE_URI_testing')

class TestConfig(unittest.TestCase):
	""" The base test class. all test Inherits from this class """

	def setUp(self):

		# db sttings
		db.drop_all()
		db.create_all()

	def tearDown(self):
		db.drop_all()

