from . import api, current_app, jsonify, request, make_response, json
from . import status, baseApi, jwt, copy
from . import adminRequired, loginRequired, loginActiveRequired, saveFile, MAX_IMEGES_NUMBER

# the logic
from . import addOperation, addCountry, getCountry, getStatus_operation, getType_operation, getOperation
from . import addPerson, addPhoto, deletePerson
from . import getUser
import datetime

@api.route('/addcountry', methods=['POST'])
@adminRequired
def addCountryRoute():
	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	countryName = post_data.get('name')
	countryPhoneCode = post_data.get('phone_code')
	countryPhoneLength = post_data.get('phone_length')
	countryIsoName = post_data.get('iso_name')
	
	# required data
	if not all([ countryName, countryPhoneCode, countryPhoneLength, countryIsoName]) :
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# make sure the Country not already exists
	if getCountry(phoneCode=countryPhoneCode):
		result['status'] = status['failure']
		result['message'] = 'Country already exists.'
		return make_response(jsonify(result), 202)

	if not addCountry(name=countryName, phoneCode=countryPhoneCode, 
					phoneLength=countryPhoneLength, isoName=countryIsoName):
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 201)


@api.route('/getcountry', methods=['GET'])
@api.route('/getcountry/<int:country_id>', methods=['GET'])
def getCountryRoute(country_id=None):
	""" Return a list of Countries or single Country with id"""

	result = copy.deepcopy(baseApi)

	if country_id:
		try:
			country_id = int(country_id)
		except Exception as e:
			result['status'] = status['failure']
			result['message'] = 'required data not submitted.'
			return make_response(jsonify(result), 400)

		country = getCountry(id=country_id)

		if not country:
			result['status'] = status['failure']
			result['message'] = 'no data found.'
			return make_response(jsonify(result), 404)

		# success
		result['status'] = status['success']
		result['data']['country'] = [country.toDict()]
		return make_response(jsonify(result), 200)

	else:
		# all Countries

		country = getCountry()


		result['status'] = status['success']
		result['data']['country'] = [c.toDict() for c in country]
		return make_response(jsonify(result), 200)

@api.route('/getstatusoperation', methods=['GET'])
@api.route('/getstatusoperation/<int:status_id>', methods=['GET'])
def getStatusOperationRoute(status_id=None):
	""" Return a list of Countries or single Country with id"""

	result = copy.deepcopy(baseApi)

	if status_id:
		try:
			status_id = int(status_id)
		except Exception as e:
			result['status'] = status['failure']
			result['message'] = 'required data not submitted.'
			return make_response(jsonify(result), 400)

		s = getStatus_operation(id=status_id)

		if not s:
			result['status'] = status['failure']
			result['message'] = 'no data found.'
			return make_response(jsonify(result), 404)

		# success
		result['status'] = status['success']
		result['data']['status_operation'] = [s.toDict()]
		return make_response(jsonify(result), 200)

	else:
		# all Countries

		s = getStatus_operation()


		result['status'] = status['success']
		result['data']['status_operation'] = [c.toDict() for c in s]
		return make_response(jsonify(result), 200)


@api.route('/gettypeoperation', methods=['GET'])
@api.route('/gettypeoperation/<int:type_id>', methods=['GET'])
def getTypeOperationRoute(type_id=None):
	""" Return a list of Countries or single Country with id"""

	result = copy.deepcopy(baseApi)

	if type_id:
		try:
			type_id = int(type_id)
		except Exception as e:
			result['status'] = status['failure']
			result['message'] = 'required data not submitted.'
			return make_response(jsonify(result), 400)

		type = getType_operation(id=type_id)

		if not type:
			result['status'] = status['failure']
			result['message'] = 'no data found.'
			return make_response(jsonify(result), 404)

		# success
		result['status'] = status['success']
		result['data']['type_operation'] = [type.toDict()]
		return make_response(jsonify(result), 200)

	else:
		# all type operation

		type = getType_operation()


		result['status'] = status['success']
		result['data']['type_operation'] = [c.toDict() for c in type]
		return make_response(jsonify(result), 200)


# helper functions to add objects
def addObjectPerson(post_data):
	""" get the prson data. return False if add person failed. 
		return the person object if added"""
	personName = post_data.get('person_name')
	age_id = post_data.get('age_id')

	# add person
	person = addPerson(name=personName, ageId=age_id)
	if not person:
		return False

	return person

def deleteObjectPerson(object):
	''' delete object'''

	return deletePerson(object=object)


object_types_add = {'Person':addObjectPerson}
object_types_delete = {'Person':deleteObjectPerson}

@api.route('/addoperation', methods=['POST'])
@loginActiveRequired
def addOperationRoute():
	""" add new operation"""

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.form

	# get the photos
	files = request.files.getlist('photos')
	
	# limit of the uploaded imeges
	if len(files) > MAX_IMEGES_NUMBER:
		result['status'] = status['failure']
		result['message']  = f'Large number of photos. no more than {MAX_IMEGES_NUMBER} photos'
		return make_response(jsonify(result), 400)


	# the user
	token = request.headers.get('token')
	try:
		payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
		userPublicId = payload['user']
	except jwt.ExpiredSignatureError :
		result['status'] = status['failure']
		result['message']  = 'Signature expired. Please log in again.'
		return make_response(jsonify(result), 202)
	except jwt.InvalidTokenError:
		result['status'] = status['failure']
		result['message']  ='Invalid token. Please log in again.'
		return make_response(jsonify(result), 202)
	

	# get 'operation-dependent' data and get sure it's valid
	date = post_data.get('date')
	if not date:
		result['status'] = status['failure']
		result['message']  = "required data 'date' not submitted"
		return make_response(jsonify(result), 400)

	# validate the date
	try:
		dateObject = datetime.datetime.strptime(date, '%Y-%m-%d')
	except Exception as e:
		result['status'] = status['failure']
		result['message']  = r'wrong date format. date must be in %Y-%m-%d fomat'
		return make_response(jsonify(result), 400)

	type_id = post_data.get('type_id')
	type = getType_operation(id=type_id)
	if not type or not type_id:
		result['status'] = status['failure']
		result['message']  = 'wrong type operation name'
		return make_response(jsonify(result), 400)
	
	status_id = post_data.get('status_id')
	
	if status_id:
		s = getStatus_operation(id=status_id)
	else:
		s = None
	
	# country of the operation
	country_id = post_data.get('country_id')
	country = getCountry(id=country_id)
	if not country:
		result['status'] = status['failure']
		result['message']  = 'wrong country name'
		return make_response(jsonify(result), 400)


	# first get the object data
	object_type = post_data.get('object_type')
	
	if not object_type or object_type not in object_types_add:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# add the object data with helper function
	object = object_types_add[object_type](post_data)

	if not object :
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. when add the object data'
		return make_response(jsonify(result), 400)
	
	# location of the item 
	lat = post_data.get('lat')
	lng = post_data.get('lng')

	# validate
	try:
		if lat or lng:
			lat = float(lat)
			lng = float(lng)
	except Exception as e:
		result['status'] = status['failure']
		result['message'] = 'lat and lng must be float numbers'
		return make_response(jsonify(result), 400)

	# get the details
	details = post_data.get('details')


	operation = addOperation(country=country, object=object, userPublicId=userPublicId,\
	 			date=dateObject, type=type, status=s, lat=lat, lng=lng, details=details)


	if not operation:
		# delete added object
		object_types_delete[object_type](object)
		
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# get the photos
	if files:
		for index, file in enumerate(files):
			# get sure no to many imeges
			if index + 1 > MAX_IMEGES_NUMBER:
				break
			
			link = saveFile(file)
			if link:
				addPhoto(link=link, object=object)
			


	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 201)


@api.route('/getoperation', methods=['GET'])
def getOperationRoute():
	""" get a list of operations"""
	result = copy.deepcopy(baseApi)
	#filters = request.view_args
	filters = request.args
	if not filters:
		# no filters
		try:
			operations = getOperation()	
		except Exception as e:
			result['status'] = status['failure']
			result['message'] = 'Some error occurred. Please try again'
			return make_response(jsonify(result), 401)

		# success
		result['status'] = status['success']
		result['data']['operations'] = [operation.toDict() for operation in operations]
		return make_response(jsonify(result), 200)

	else:
		# with filters
		if 'user' in filters:
			user = getUser(userPublicId=filters['user'])
			
			if not user:
				result['status'] = status['failure']
				result['message'] = "not valid filter 'user'"
				return make_response(jsonify(result), 400)

			filters['user_id'] = user.id
			del filters['user']

		if 'date' in filters:
			# make sure the date have the rigth fromat
			try:
				filters['date'] = datetime.datetime.strptime(date, '%Y-%m-%d')
			except Exception as e:
				result['status'] = status['failure']
				result['message']  = 'wrong date format. date must be in %Y-%m-%d fomat'
				return make_response(jsonify(result), 400)

		try:
			operations = getOperation(**filters)
		except Exception as e:
			result['status'] = status['failure']
			result['message']  = e
			return make_response(jsonify(result), 400)
		
		# success
		result['status'] = status['success']
		result['data']['operations'] = [operation.toDict() for operation in operations]
		return make_response(jsonify(result), 200)


