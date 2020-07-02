from ..models import db, Operations, Type_operation, Status_operation, Country, Users


# Country model
def addCountry(name, phoneCode):
	""" return the country objecct if country added correctly else False """
	try:
		country = Country(name=name, phone_code=phoneCode)

		db.session.add(country)
		db.session.commit()
	
	except Exception as e:
		return False

	return country

def getCountry(id=None, name=None, phoneCode=None):
	""" return the country object or None if not exist
		return a list of all countries if no perm passed"""

	if not any([id, name, phoneCode]):
		return Country.query.all()
	if id :
		return Country.query.get(id)
	if name:
		return Country.query.filter_by(name=name).first()
	if phoneCode:
		return Country.query.filter_by(phone_code=phoneCode).first()

	return None

# Status_operation model
def addStatus_operation(name):
	""" return the new Status operation object added correctly else False """
	try:
		status = Status_operation(name=name)

		db.session.add(status)
		db.session.commit()
	
	except Exception as e:
		return False

	return status

def getStatus_operation(id=None, name=None):
	""" return the Status object or None if not exist
		return a list of all Status if no perm passed"""

	if not any([id, name]):
		return Status_operation.query.all()
	if id :
		return Status_operation.query.get(id)
	if name:
		return Status_operation.query.filter_by(name=name).first()	

	return None

# Type_operation model
def addType_operation(name):
	""" return the Type operation object added correctly else False """
	try:
		type = Type_operation(name=name)

		db.session.add(type)
		db.session.commit()
	
	except Exception as e:
		return False

	return type

def getType_operation(id=None, name=None):
	""" return the Type object or None if not exist
		return a list of all Types if no perm passed"""

	if not any([id, name]):
		return Type_operation.query.all()
	if id :
		return Type_operation.query.get(id)
	if name:
		return Type_operation.query.filter_by(name=name).first()
	

	return None

# Operations model
def addOperation(country, object, userPublicId, date, type=None, status=None, lat=None, lng=None):
	
	""" return the new Operation object added correctly else False.
		perm: country 		= the Country object 
		perm: object 		= the object this Operation dealing with as Model object
		perm: userPublicId 	= the user responsible of this Operation
		perm: date 			= the date of this Operation
		
		perm: type			= the Type_operation object 
		perm: status_id 	= the  Status_operation object
		perm: lat 			= the lat of this Operation
		perm: lng 			= the lng of this Operation"""
	
	try:
		operation = Operations(object = object, date = date)
		if lat:
			operation.lat = lat
		if lng:
			operation.lng = lng

		if not type:
			type = getType_operation(name='lost')
		

		if not status:
			status = getStatus_operation(name='active')
		

		
		# get the depended objects
		user = Users.query.filter_by(public_id=userPublicId).first()
		

		user.operations.append(operation)
		type.operations.append(operation)
		status.operations.append(operation)
		country.operations.append(operation)

		db.session.add(operation)
		db.session.commit()
		
	except Exception as e:
		return False

	return operation

