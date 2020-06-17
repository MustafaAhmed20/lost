from . import db

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.TEXT, unique=True)
	
	name = db.Column(db.String(80), nullable=False)
	password = db.Column(db.TEXT, nullable=False)
	
	phone = db.Column(db.TEXT)
		
	permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

	status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

class Status(db.Model):
	""" This table represent the statuses of the user
		active , wait activation or inactive"""

	__tablename__ = 'status'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), nullable=False)

	users = db.relationship('Users', backref='status', lazy='dynamic')

class Permission(db.Model):
	"""permission table for the users"""
	
	__tablename__ = 'permission'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)

	users = db.relationship('Users', backref='permission', lazy='dynamic')