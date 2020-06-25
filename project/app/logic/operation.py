from ..models import db, Operations, Type_operation, Status_operation, Country, Users


# Country model
def addCountry(name, phoneCode):
	""" return True if country added correctly else False """
	try:
		country = Country(name=name, phone_code=phoneCode)

		db.session.add(country)
		db.session.commit()
	
	except Exception as e:
		return False

	return True

# Status_operation model
def addStatus_operation(name):
	""" return True if Status operation added correctly else False """
	try:
		status = Status_operation(name=name)

		db.session.add(status)
		db.session.commit()
	
	except Exception as e:
		return False

	return True

# Type_operation model
def addType_operation(name):
	""" return True if Type operation added correctly else False """
	try:
		type = Type_operation(name=name)

		db.session.add(type)
		db.session.commit()
	
	except Exception as e:
		return False

	return True

# Operations model
def addOperation(type_id, status_id, country_id, object, userPublicId, date,lat=None, lng=None):
	
	""" return True if Operation added correctly else False.
		perm: type_id 		= the Foreign Key to Type_operation table
		perm: status_id 	= the Foreign Key to Status_operation table
		perm: country_id 	= the Foreign Key to Country table
		perm: object 		= the object this Operation dealing with as Model object
		perm: userPublicId 	= the user responsible of this Operation
		perm: date 			= the date of this Operation
		perm: lat 			= the lat of this Operation
		perm: lng 			= the lng of this Operation"""
	
	try:
		operation = Operations(object = object, date = date)
		if lat:
			operation.lat = lat
		if lng:
			operation.lng = lng

		# get the depended objects
		user = Users.query.filter_by(public_id=userPublicId).first()
		type = Type_operation.query.get(type_id)
		status = Status_operation.query.get(status_id)
		country = Country.query.get(country_id)

		
		user.operations.append(operation)
		type.operations.append(operation)
		status.operations.append(operation)
		country.operations.append(operation)

		db.session.add(operation)
		db.session.commit()
		
	except Exception as e:
		return False

	return True

