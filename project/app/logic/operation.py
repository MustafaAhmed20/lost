from ..models import db, Operations, Type_operation, Status_operation, Country, Users

# import all the class that operation can use it as object
from ..models import Person, Car, Accident, PersonalBelongings

# Country model
def addCountry(name, phoneCode, phoneLength, isoName):
	""" return the country objecct if country added correctly else False """
	try:
		country = Country(name=name, phone_code=phoneCode, phone_length=phoneLength, iso_name=isoName)

		db.session.add(country)
		db.session.commit()
	
	except Exception as e:
		return False

	return country

def getCountry(id=None, name=None, phoneCode=None, isoName=None):
	""" return the country object or None if not exist
		return a list of all countries if no perm passed"""

	if not any([id, name, phoneCode, isoName]):
		return Country.query.all()
	if id :
		return Country.query.get(id)
	if name:
		return Country.query.filter_by(name=name).first()
	if phoneCode:
		return Country.query.filter_by(phone_code=phoneCode).first()
	if isoName:
		return Country.query.filter_by(iso_name=isoName).first()

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
def addOperation(country, object, userPublicId, date, type=None, status=None, lat=None,state=None, city=None, lng=None, details=None):
	
	""" return the new Operation object added correctly else False.
		perm: country 		= the Country object 
		perm: object 		= the object this Operation dealing with as Model object
		perm: userPublicId 	= the user responsible of this Operation
		perm: date 			= the date of this Operation
		
		perm: type			= the Type_operation object 
		perm: status_id 	= the  Status_operation object
		perm: lat 			= the lat of this Operation
		perm: lng 			= the lng of this Operation
		perm: state 		= the location(state) of this Operation
		perm: city 			= the location(city) of this Operation
		perm: details 		= the details of this Operation"""
	
	try:
		operation = Operations(object=object, date=date, state=state, city=city)
		if lat:
			operation.lat = float(lat)
		if lng:
			operation.lng = float(lng)
		if details:
			operation.details = details

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

def getOperation(**filters):
	""" return the Operation object if filtered with id object or None if not exist. 
		return a list of Operations objects with filters apply	
		return a list of all Operations if no filters passed
		ignore all not valid filters
		
		filters :
		id 			:Operation id
		country_id	:country id of the  
		object 		:object type of the Operation
		user_id 	:user id who responsible of the Operation
		date 		:date of the Operation

	 	add_date 	:add-to-system date
	 	type_id		:type id of the Operation
	 	status_id	:status id of the Operation
	 	lat 		:lat of the Operation
	 	lng			:lng of the Operation
		"""

	availableFilters = ['id', 'country_id', 'object', 'user_id', 'date',\
	 'add_date', 'type_id', 'status_id', 'lat', 'lng']

	allowedFilters = {}

	for filter in filters:
		if filter not in availableFilters:
			# ignore the wrong filters
			pass
		else:
			# add the filter immediately if the filter is not list - this was a fix for server bug that pass the 
			# string filter as a list of letters
			allowedFilters[filter] = ''.join(filters[filter]) if type(filters[filter]) is list else filters[filter]


	baseQuery = Operations.query
	
	if not allowedFilters:
		return baseQuery.all()

	if 'id' in allowedFilters:
		return baseQuery.get(allowedFilters['id'])

	if 'object' in allowedFilters:

		try:
			object = eval(allowedFilters['object'])

			baseQuery = baseQuery.filter(Operations.object.is_type(object))

		except Exception as e:	
			return None

		del allowedFilters['object']
	
	try:
		if 'lat' in allowedFilters:
			allowedFilters['lat'] = float(allowedFilters['lat'])
		if 'lng' in allowedFilters:
			allowedFilters['lng'] = float(allowedFilters['lng'])
	except Exception as e:
		del allowedFilters['lat']
		del allowedFilters['lng']
		pass

	return baseQuery.filter_by(**allowedFilters).all()

def updateOperationStatus(newStatus, operation=None, operationId=None):
	''' update operation status - return true is success else false'''

	if not operationId and not operation:
		raise ValueError('operation object or operationId is required')

	# first get the operation
	if operationId:
		operation = Operations.query.get(operationId)

	if not operation:
		return False

	StatusOperation = Status_operation.query.filter_by(name=newStatus).first()

	if not StatusOperation:
		return False

	StatusOperation.operations.append(operation)
	db.session.commit()
	return True


