from ..models import db, Users, Status, Permission
from ..extensions import check_password_hash, generate_password_hash
import uuid


def login(userPhone, userPassword):
	""" return True if the phone and the password are correct!"""
	
	# check if the user exist .
	user = Users.query.filter_by(phone=userPhone).first()
	if not user:
		return False

	# check if the password is correct
	if not check_password_hash(user.password, userPassword):
		return False

	return True

def addUser(name, phone, password, status='active', permission='user'):
	""" return True if user added correctly else False """
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

		return True
	
	except Exception as e:
		
		return False
	
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

