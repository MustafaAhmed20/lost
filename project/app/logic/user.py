from ..models import db, Users, Status, Permission, UserVerificationNumber
from ..extensions import check_password_hash, generate_password_hash, datetime

import uuid
import random

# User model
def login(userPhone, userPassword):
	""" return True if the phone and the password are correct!"""
	
	# check if the user exist .
	user = Users.query.filter_by(phone=userPhone).first()
	if not user:
		return False

	# check if the password is correct
	if not check_password_hash(user.password, str(userPassword)):
		return False

	return True

def addUser(name, phone, password, status='active', permission='user'):
	""" return The new user object if user added correctly else False """
	try:
		user = Users(name=name, password=generate_password_hash(str(password)),
				public_id=uuid.uuid4, phone=phone)

		status_user = Status.query.filter_by(name=status).first()
		permission_user = Permission.query.filter_by(name=permission).first()

		# default status or permission if not valid status or permission
		if not status_user:
			status_user = Status.query.filter_by(name='active').first()

		if not permission_user:
			permission_user = Permission.query.filter_by(name='user').first()

		status_user.users.append(user)
		permission_user.users.append(user)

		db.session.add(user)
		db.session.commit()

		return user
	
	except Exception as e:
		
		return False

def registerUser(name, phone, password):
	''' register new User with 'wait activation' Status 
		return (user, code) if success else false'''

	result = addUser(name, phone, password, status='wait', permission='user')

	if result:
		# add Verification Number to the user

		while True:
			# check the random if it is unique or not
			number = ''.join([str(random.randint(0,9)) for _ in range(6)])
			object = UserVerificationNumber.query.filter_by(code=number).first()
			if object:
				# repete
				continue
			code = UserVerificationNumber(code=number, user_id=result.id)

			# save the code
			db.session.add(code)
			db.session.commit()
			break

		return result, code

	else:
		return result

def VerifyUser(code, user_id=None, userPublicId=None, maxTimeDays=1):
	''' if code is correct change user Status to 'active' '''

	if maxTimeDays < 1:
		raise  ValueError('not valid days difference')

	if not any([user_id, userPublicId]):
		raise  ValueError('no user data passed')

	# check if the user exist .
	if user_id:
		user = Users.query.get(user_id)
	elif userPublicId:
		user = Users.query.filter_by(public_id=userPublicId).first()
	
	if not user:
		return False		

	# get the Verification details
	VerifyCode = UserVerificationNumber.query.filter_by(user_id=user.id).first()

	# no code for this user
	if not VerifyCode:
		return False

	# check if its to late
	now = datetime.datetime.now()

	diff = now - VerifyCode.create_date

	if diff.days >= maxTimeDays:
		# to late
		# delete the code
		db.session.delete(VerifyCode)
		return False

	# check the code

	if code.replace(' ', '') != VerifyCode.code:
		return False

	# delete the Verify Code
	db.session.delete(VerifyCode)

	# make the user active
	return changeUserStatus(user.public_id, 'active')

def changeUserPermission(userPublicId, toPermission):
	"""change the User Permission"""

	# check if the user exist .
	user = Users.query.filter_by(public_id=userPublicId).first()
	if not user:
		return False

	permission = Permission.query.filter_by(name=toPermission).first()

	if permission:
		permission.users.append(user)
		db.session.commit()
		return True
	return False

def changeUserStatus(userPublicId, toStatus):
	"""change the User Permission"""

	# check if the user exist .
	user = Users.query.filter_by(public_id=userPublicId).first()
	if not user:
		return False

	status = Status.query.filter_by(name=toStatus).first()

	if status:
		status.users.append(user)
		db.session.commit()
		return True
	return False

def getUser(id=None, publicId =None, phone=None):
	""" return the user object or None if not exist"""
	if not any ([id, publicId, phone]):
		return None

	if id :
		return Users.query.get(id)

	if publicId:
		return Users.query.filter_by(public_id=publicId).first()

	if phone:
		return Users.query.filter_by(phone=phone).first()		

# Status model
def addStatus(name):
	""" add new user Status 
	return the new status object if added or false if failed"""
	try:
		status = Status(name=name)

		db.session.add(status)
		db.session.commit()	
	except Exception as e:
		return False
	

	return status

# Permission model
def addPermission(name):
	""" add new user Status 
	return the new permission object if added or false if failed"""
	try:
		permission = Permission(name=name)

		db.session.add(permission)
		db.session.commit()	
	except Exception as e:
		return False
	

	return permission
