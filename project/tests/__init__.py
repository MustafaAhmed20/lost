from app import create_app

from app.models import db, defaultData

import unittest
import os


app = create_app()
app.app_context().push()

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') +\
										 os.getenv('DATABASE_NAME_TESTING')

# raise error if no environment variable
assert os.getenv('SQLALCHEMY_DATABASE_URI') and os.getenv('DATABASE_NAME_TESTING')

class TestConfig(unittest.TestCase):
	""" The base test class. all test Inherits from this class """

	def setUp(self):
		"""
		Create the database if not created!
		
		NOTE: this part work with mysql database, 
		if you use any other database you may consider this part and make the necessary changes
		"""
		
		self.client_app = app.test_client()
		
		try:
			db.drop_all()
			
		except Exception as e:
			from flask_sqlalchemy import sqlalchemy
			e = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
			
			existing_databases = e.execute("SHOW DATABASES;")
			# Results are a list of single item tuples, so unpack each tuple
			existing_databases = [d[0] for d in existing_databases]

			# Create database if not exists
			if os.getenv('DATABASE_NAME_TESTING') not in existing_databases:

				e.execute(f"CREATE DATABASE {os.getenv('DATABASE_NAME_TESTING')}")
				# do it again
				db.drop_all()

		# now create the tables 
		db.create_all()

		# add the default Data
		defaultData(app=app, db=db)

	def tearDown(self):
		db.drop_all()
