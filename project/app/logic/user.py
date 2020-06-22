from . import User
from .. import check_password_hash, generate_password_hash

def login(userPhone, userPassword):
	""" return True if the phone and the password are correct!"""
	# check if the user exist .
	user = User.query.filter_by(phone=userPhone).first()
	if not user:
		return False

	# check if the password is correct
	if not check_password_hash(user.password, userPassword):
		return False

	return True

def addUser(name, phone):
	pass
