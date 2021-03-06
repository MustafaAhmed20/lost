from . import db, generic_relationship
from .person import Photos
from . import datetime

# user class
from . import Users

class Operations(db.Model):
	""" The main table represents the operations in the app"""
	__name__ = 'Operations'
	__tablename__ = 'operations'
	id = db.Column(db.Integer, primary_key=True)

	# date and time of add to the system
	add_date = db.Column(db.DATETIME(timezone=True), default=datetime.datetime.utcnow)

	# date of operation (lost or found)
	date = db.Column(db.DATE, nullable=False)

	# the user created this operation
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	# location of the item or the persion that get lost or found
	lat = db.Column(db.DECIMAL(precision=12, scale=8)) 
	lng = db.Column(db.DECIMAL(precision=12, scale=8))

	# location as Text
	state = db.Column(db.TEXT)
	city = db.Column(db.TEXT)

	# the details of the operation
	details = db.Column(db.TEXT)

	# This is used to discriminate between the linked tables.
	object_type = db.Column(db.Unicode(255))

	# This is used to point to the primary key of the linked row.
	object_id = db.Column(db.Integer)

	# this this used to connect to object desired like(person - car - etc)
	object = generic_relationship(object_type, object_id)

	# type of the operation
	type_id = db.Column(db.Integer, db.ForeignKey('type_operation.id'), nullable=False)

	# status of the operation
	status_id = db.Column(db.Integer, db.ForeignKey('status_operation.id'), nullable=False)

	# country of the operation
	country_id = db.Column(db.Integer,  db.ForeignKey('country.id'), nullable=False)

	# the comments of this operation
	comments = db.relationship('Comment', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id,
				'date':self.date.strftime ('%Y-%m-%d'),
				'add_date':self.add_date.replace(tzinfo=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z'),
				'object_type':self.object.__name__, 'object':self.object.toDict(),
				'country_id':self.country_id,
				'type_id':self.type_id, 'status_id':self.status_id,
				'lat':float(self.lat) if self.lat else None,
				'lng':float(self.lng) if self.lng else None,
				'state': self.state, 'city': self.city,
				'details': self.details,
				'user': Users.query.get(self.user_id).toDict(),
				'photos':[photo.link for photo in Photos.query.filter_by(object=self.object).all()]}

class Type_operation(db.Model):
	"""Define the type of the operation. (lost - found)"""
	__name__ = 'Type_operation'
	__tablename__ = 'type_operation'
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(20), nullable=False, unique=True)

	operations = db.relationship('Operations', backref='type', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name}

class Status_operation(db.Model):
	"""Define the status of the operation. (active - on hold - closed)"""
	__name__ = 'Status_operation'
	__tablename__ = 'status_operation'
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(20), nullable=False, unique=True)

	operations = db.relationship('Operations', backref='status', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name}

class Country(db.Model):
	"""represents the countries that  the app operating in"""
	__name__ = 'Country'
	__tablename__ = 'country'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)
	phone_code = db.Column(db.Integer, unique=True)

	# the max length of the phone number without the beginning zero
	phone_length = db.Column(db.Integer, nullable=False)

	# the iso name for the country. ex(EG)
	iso_name = db.Column(db.String(4), nullable=False, unique=True)

	operations = db.relationship('Operations', backref='country', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name, 
				'phone_code':self.phone_code, 'phone_length':self.phone_length,
				'iso_name':self.iso_name}
