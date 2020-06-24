from . import db, generic_relationship

class Person(db.Model):
	__tablename__ = 'person'
	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(80))
	
	age_id = db.Column(db.Integer, db.ForeignKey('age.id'))

class Age(db.Model):
	"""This table represents the age ranges for persons"""
	__tablename__ = 'age'
	id = db.Column(db.Integer, primary_key=True)

	# the age range
	min_age = db.Column(db.Integer, nullable=False)
	max_age = db.Column(db.Integer, nullable=False)

	persons = db.relationship('Person', backref='age', lazy='dynamic')

class Photos(db.Model):
	"""store the links of the photos and the object that this photo belong to"""
	__tablename__ = 'photos'
	id = db.Column(db.Integer, primary_key=True)

	#link to the photo
	link = db.Column(db.TEXT)

	# This is used to discriminate between the linked tables.
	object_type = db.Column(db.Unicode(255))

	# This is used to point to the primary key of the linked row.
	object_id = db.Column(db.Integer)

	object = generic_relationship(object_type, object_id)
