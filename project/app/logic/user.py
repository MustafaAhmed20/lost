from ..models import db, Users, Status, Permission, UserVerificationNumber, LoginDeviceIds
from ..extensions import check_password_hash, generate_password_hash, datetime

import uuid
import random

##
# in test mode the sms code is accebteble if the user logged-in from the same device
##

TEST_MODE:bool = True

# helper fuctions
def _createVerifyCode():
	''' create unique 6 digit code number as str''' 
	while True:
		# check the random if it is unique or not
		code = ''.join([str(random.randint(0,9)) for _ in range(6)])
		object = UserVerificationNumber.query.filter_by(code=code).first()
		if object:
			# repete
			continue
		break
	return code

def _checkCode(user_id, code, maxTimeDays=1, deleteCode=False, deviceID:str =''):
	''' check if the code is exist or not with the user
		if deleteCode set to True then the code will be deleted in case if success
		return True if its valid code else False
		NOTE: the code will be deleted if its expired'''

	# TODO: delete this after activate the sms code
	if TEST_MODE and deviceID:
		# check if the user logged-in with this user before
		user = Users.query.get(user_id)
		if user:
			return _checkLoginUserWithDevice(user=user, deviceID=deviceID)
		

	# get the Verification details
	VerifyCode = UserVerificationNumber.query.filter_by(user_id=user_id).first()

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

	# delete code if deleteCode set to true
	if deleteCode:
		# delete the Verify Code
		db.session.delete(VerifyCode)

	# succes
	return True

def _restPassword(user_id, newPassword):
	''' return True is success else False'''
	# check if the user exist .
	user = Users.query.get(user_id)
	if not user:
		return False

	user.password = generate_password_hash(newPassword)
	db.session.commit()

	return True

def _deleteUserCode(user_id):
	# delete all codes for this user

	# delete the Verification details
	VerifyCode = UserVerificationNumber.query.filter_by(user_id=user_id).delete()

	db.session.commit()

	return True

def _createPublicId():
	''' return unique public id for users'''

	while True:
		code = str(uuid.uuid4())
		user = Users.query.filter_by(public_id=code).first()
		if user:
			# repete
			continue
		# unique
		return code

# login the user with the device
def _loginUserWithDevice(userPhone:str, deviceID:str):

	user = Users.query.filter_by(phone=userPhone).first()

	if not user:
		return

	# get the device if found before
	device = LoginDeviceIds.query.filter_by(device_id=deviceID).first()

	if not device:
		device = LoginDeviceIds(device_id=deviceID)

		db.session.add(device)
		db.session.commit()

	# add to the user devices
	user.devices.append(device)

def _checkLoginUserWithDevice(user:Users, deviceID:str)-> bool:
	'''check if the user logged with this device before'''
	
	device = LoginDeviceIds.query.filter_by(device_id=deviceID).first()

	if not device:
		return False
	
	if device in user.devices:
		return True

	return False


# User model
def login(userPhone, userPassword, deviceID: str = ''):
	""" return True if the phone and the password are correct!"""
	
	# check if the user exist .
	user = Users.query.filter_by(phone=userPhone).first()
	if not user:
		return False

	# check if the password is correct
	if not check_password_hash(user.password, str(userPassword)):
		return False

	if deviceID:
		# register the user login with this device
		_loginUserWithDevice(userPhone=userPhone, deviceID=deviceID)

	return True

def addUser(name, phone, password, status='active', permission='user'):
	""" return The new user object if user added correctly else False """
	try:
		user = Users(name=name, password=generate_password_hash(str(password)),
				public_id=_createPublicId(), phone=phone)

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
		


def updateUserData(user, name=None, newPassword=None, password=None):
	'''the user update his data, phone not changable
		return True if success else False
		perm user: the user object'''
	if not any([name, newPassword, password]):
		# no data passed
		return False

	if newPassword:
		if not password:
			return False
		# check the old password
		if not check_password_hash(user.password, str(password)):
			return False
		# change the password
		user.password = generate_password_hash(str(newPassword))
		if name:
			user.name = name
		db.session.commit()
		return True

	# no password - just name
	user.name = name
	db.session.commit()
	return True

def registerUser(phone, password, name=None):
	''' register new User with 'wait activation' Status 
		return (user, code) if success else false'''

	#result = addUser(name, phone, password, status='wait', permission='user')
	result = addUser(name, phone, password, status='active', permission='user')

	# stop code Verification
	return result, None

	# if result:
	# 	# add Verification Number to the user

	# 	number = _createVerifyCode()

	# 	code = UserVerificationNumber(code=number, user_id=result.id)

	# 	# save the code
	# 	db.session.add(code)
	# 	db.session.commit()

	# 	return result, code

	# else:
	# 	return result

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

	valid = _checkCode(user.id, code, maxTimeDays=maxTimeDays, deleteCode=False)

	if not valid:
		return False

	# make the user active
	changeUserStatus(user.public_id, 'active')
	return True

def forgotPassword(phone):
	''' check if there is a user with this phone then create code to him
		return 'UserVerificationNumber' object '''

	# check if the user exist .
	user = Users.query.filter_by(phone=phone).first()
	if not user:
		return False

	# delete old codes for this user
	_deleteUserCode(user_id=user.id)

	code = _createVerifyCode()

	# save the code with this user
	userCode = UserVerificationNumber(code=code, user_id=user.id)

	# save the code
	db.session.add(userCode)
	db.session.commit()

	return userCode

def resetPassword(code, phone, newPassword=None, deviceID: str = ''):
	''' check if the code is valid or not, if newPassword given it will be reset'''
	# first get the user
	user = Users.query.filter_by(phone=phone).first()
	if not user:
		return False

	# check the code
	if not _checkCode(user.id, code, deleteCode=bool(newPassword), deviceID=deviceID):
		# if code not valid
		return False

	# if the new password passed
	if newPassword:
		_restPassword(user.id, newPassword)

	# succes
	return True



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
	"""change the User Status"""

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

def getStatus(name=None):
	""" return the Status object or None if not exist
		return all if not name passed."""
	
	if not name:
		return Status.query.all()

	return Status.query.filter_by(name=name).first()

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

def getPermission(name=None):
	""" return the Status object or None if not exist
		return all if not name passed."""
	
	if not name:
		return Permission.query.all()

	return Permission.query.filter_by(name=name).first()
