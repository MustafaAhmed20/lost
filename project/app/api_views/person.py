from . import api, current_app, jsonify, request, make_response, json
from . import status, baseApi
from . import adminRequired

# the logic
from . import addPerson, deletePerson, addAge, addPhoto, getAge

@api.route('/addage', methods=['POST'])
@adminRequired
def addAgetRoute():
	""" add new age range """
	
	# the retuned response
	result = baseApi.copy()

	# get the post data
	post_data = request.get_json()
	
	min_age = post_data.get('minage')
	max_age = post_data.get('maxage')
	
	if not min_age or not max_age:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# make sure the age not already exists
	if getAge(minAge=min_age, maxAge=max_age):
		result['status'] = status['failure']
		result['message'] = 'Age already exists.'
		return make_response(jsonify(result), 202)

	if not addAge(minAge=min_age, maxAge=max_age):
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 201)

