from . import db

class Person(db.Model):
	__tablename__ = 'person'
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(80))
	
	photos = db.Column(db.TEXT)

	age_id = db.Column(db.Integer, db.ForeignKey('age.id'))

	# the photos of the person
	photos = db.relationship('Photos', lazy='dynamic')

	operation = db.relationship('Operations', lazy='dynamic', backref='person', uselist=False)

class Age(db.Model):
	"""This table represents the age ranges for persons"""
	__tablename__ = 'age'
	id = db.Column(db.Integer, primary_key=True)

	# the age range
	min_age = db.Column(db.Integer, nullable=False)
	max_age = db.Column(db.Integer, nullable=False)

	persons = db.relationship('Persons', backref='age', lazy='dynamic')

class Photos(db.Model):
	""""""
	__tablename__ = 'photos'
	id = db.Column(db.Integer, primary_key=True)

	#link to the photo
	link = db.Column(db.TEXT)
