from . import db
from . import datetime

# devices secoundry table
association_user_device_table = db.Table('association_user_device', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('device_id', db.Integer, db.ForeignKey('login_device_ids.id'))
)

class Users(db.Model):
	__name__ = 'Users'
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(50), unique=True)
	
	name = db.Column(db.String(80))
	password = db.Column(db.TEXT, nullable=False)
	
	phone = db.Column(db.String(12), nullable=False, unique=True)
		
	permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))

	status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

	# the operations this user created
	operations = db.relationship('Operations', backref='user', lazy='dynamic')

	# the comments made by this user
	comments = db.relationship('Comment', lazy='dynamic')

	# the devices that the user logged-in with
	devices = db.relationship(
        "LoginDeviceIds",
        secondary = association_user_device_table,
        back_populates = "users")

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.public_id, 'name':self.name, 'phone':self.phone, 'permission':self.permission_id,\
				'status':self.status_id}

class Status(db.Model):
	""" This table represent the statuses of the user
		active , wait activation or inactive"""
	__name__ = 'Status'
	__tablename__ = 'status'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(10), nullable=False, unique=True)

	users = db.relationship('Users', backref='status', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name}

class Permission(db.Model):
	"""permission table for the users"""
	__name__ = 'Permission'
	__tablename__ = 'permission'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)

	users = db.relationship('Users', backref='permission', lazy='dynamic')

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'name':self.name}

class UserVerificationNumber(db.Model):
	''' this model used to save Verification Numbers'''

	__name__ = 'UserVerificationNumber'
	__tablename__ = 'user_verification_number'

	id = db.Column(db.Integer, primary_key=True)
	
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	code =  db.Column(db.String(10), nullable=False, unique=True)

	create_date = db.Column(db.DATETIME, default=datetime.datetime.utcnow)

class LoginDeviceIds(db.Model):
	''' This model used to save ids of the Devices that logged-in'''

	__name__ = 'LoginDeviceIds'
	__tablename__ = 'login_device_ids'

	id = db.Column(db.Integer, primary_key=True)

	device_id = db.Column(db.String(20), nullable=False, unique=True)

	users = db.relationship(
        "Users",
        secondary = association_user_device_table,
        back_populates = "devices")
