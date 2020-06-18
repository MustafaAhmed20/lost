from . import db
from . import datetime

class Operations(db.Model):
	""" The main table represents the operations in the app"""

	__tablename__ = 'operations'
	id = db.Column(db.Integer, primary_key=True)

	# type of the operation
	type_id = db.Column(db.Integer, db.ForeignKey('type_operation.id'))

	# status of the operation
	status_id = db.Column(db.Integer, db.ForeignKey('status_operation.id'))

	# country of the operation
	country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

	# date of add to the system
	add_date = db.Column(db.DATETIME, default=datetime.datetime.now())

	# date of operation (lost or found)
	date = db.Column(db.DATETIME, nullable=False)

	# the user created this operation
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	# location of the item or the persion that get lost or found
	lat = db.Column(db.Float(10,6))
	lng = db.Column(db.Float(10,6))

	# the person 
	person = db.Column(db.Integer, db.ForeignKey('person.id'))

class Type_operation(object):
	"""Define the type of the operation. (lost - found)"""
	__tablename__ = 'type_operation'
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(20), nullable=False)

	operations = db.relationship('Operations', backref='type', lazy='dynamic')

class Status_operation(object):
	"""Define the status of the operation. (active - on hold - closed)"""
	__tablename__ = 'status_operation'
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(20), nullable=False)

	operations = db.relationship('Operations', backref='status', lazy='dynamic')

class Country(object):
	"""represents the countries that  the app operating in"""
	__tablename__ = 'country'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)

	operations = db.relationship('Operations', backref='country', lazy='dynamic')
