from ..extensions import SQLAlchemy
from ..extensions import datetime, generate_password_hash, generic_relationship
import os
import uuid

db =  SQLAlchemy()


from .user import *
from .operation import *
from .person import *

def defaultData(app, db):
	""" the default data in the databas"""
	
	app.app_context().push()

	# defult data
	sudan = Country(name='sudan', phone_code='249')
	egypt = Country(name='egypt', phone_code='20')

	active = Status_operation(name='active')
	on_hold = Status_operation(name='on_hold')
	closed = Status_operation(name='closed')

	lost = Type_operation(name='lost')
	found = Type_operation(name='found')

	#user
	active_user = Status(name='active')
	wait = Status(name='wait')
	in_active = Status(name='in_active')

	admin = Permission(name='admin')
	manager = Permission(name='manager')
	normal_user = Permission(name='user')

	admin_user = Users(name='admin', phone=os.getenv('admin_phone'), 
						password=generate_password_hash(os.getenv('admin_pass')),
						public_id=uuid.uuid4())

	active_user.users.append(admin_user)
	admin.users.append(admin_user)

	# age
	first_age = Age(min_age=1, max_age=10)
	secound_age = Age(min_age=10, max_age=20)

	db.session.add(sudan)
	db.session.add(egypt)
	
	db.session.add(active)
	db.session.add(on_hold)
	db.session.add(closed)
	
	db.session.add(lost)
	db.session.add(found)
	
	db.session.add(active_user)
	db.session.add(wait)
	db.session.add(in_active)
	db.session.add(admin)
	db.session.add(manager)
	db.session.add(normal_user)
	db.session.add(admin_user)
	
	db.session.add(first_age)
	db.session.add(secound_age)
	db.session.commit()

