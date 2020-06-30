from . import api, current_app, jsonify, request, make_response, json
from . import status, baseApi
from . import adminRequired, loginRequired

# the logic
from . import addOperation, addCountry, getCountry, getStatus_operation, getType_operation

@api.route('/addoperation', methods=['POST'])
@loginRequired
def addOperationRoute():
	pass


@api.route('/addcountry', methods=['POST'])
@loginRequired
def addCountryRoute():
	# the retuned response
	result = baseApi.copy()

	# get the post data
	post_data = request.get_json()

	countryName = post_data.get('name')
	countryPhoneCode = post_data.get('phonecode')
	
	
	if not countryName or not countryPhoneCode:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# make sure the user not already exists
	if getCountry(phoneCode=countryPhoneCode):
		result['status'] = status['failure']
		result['message'] = 'Country already exists. Please Log in.'
		return make_response(jsonify(result), 202)

	if not addCountry(name=countryName, phoneCode=countryPhoneCode):
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

	result = baseApi.copy()

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

	result = baseApi.copy()

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
		result['data']['statusoperation'] = [s.toDict()]
		return make_response(jsonify(result), 200)

	else:
		# all Countries

		s = getStatus_operation()


		result['status'] = status['success']
		result['data']['statusoperation'] = [c.toDict() for c in s]
		return make_response(jsonify(result), 200)


@api.route('/gettypeoperation', methods=['GET'])
@api.route('/gettypeoperation/<int:type_id>', methods=['GET'])
def getTypeOperationRoute(type_id=None):
	""" Return a list of Countries or single Country with id"""

	result = baseApi.copy()

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
		result['data']['typeoperation'] = [type.toDict()]
		return make_response(jsonify(result), 200)

	else:
		# all type operation

		type = getType_operation()


		result['status'] = status['success']
		result['data']['typeoperation'] = [c.toDict() for c in type]
		return make_response(jsonify(result), 200)
