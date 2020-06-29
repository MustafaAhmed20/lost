from . import db

class Users(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	
	name = db.Column(db.String(80), nullable=False)
	password = db.Column(db.TEXT, nullable=False)
	
	phone = db.Column(db.String(12), nullable=False, unique=True)
		
	permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

	status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

	# the operations this user created
	operations = db.relationship('Operations', backref='user', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.public_id, 'name':self.name, 'phone':self.phone, 'permissio':permission_id,\
				'status':status_id}

class Status(db.Model):
	""" This table represent the statuses of the user
		active , wait activation or inactive"""

	__tablename__ = 'status'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), nullable=False, unique=True)

	users = db.relationship('Users', backref='status', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name}

class Permission(db.Model):
	"""permission table for the users"""
	
	__tablename__ = 'permission'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)

	users = db.relationship('Users', backref='permission', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name}

