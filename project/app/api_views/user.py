from . import api, current_app, jsonify, request, make_response, json
from . import days, minutes, status, baseApi
from . import adminRequired
from ..extensions import jwt
import datetime

# the logic
from . import login, getUser, addUser, getCountry, validatePassword, validatePhoneNumber

# the shortest length for passwords
MIN_PASSWORD_LENGTH = 5

@api.route('/login', methods=['POST'])
def loginUserRoute():
	result = baseApi.copy()

	# get the post data
	post_data = request.get_json()
	try:
		phone = post_data.get('phone')
		password = post_data.get('password')

		# this used to validate the phone number
		userCountryID = post_data.get('country_id')
	except Exception as e:

		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	
	if not phone or not password or not userCountryID:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# validate the phone number
	# ..
	# first git the country
	country = getCountry(id=userCountryID)
	if not country:
		result['status'] = status['failure']
		result['message']  = 'wrong country name'
		return make_response(jsonify(result), 400)
	# now validate
	phone = validatePhoneNumber(phone, country.phone_code, country.phone_length)
	if not phone:
		result['status'] = status['failure']
		result['message'] = 'phone number not pass the validation'
		return make_response(jsonify(result), 400)

	if login(userPhone=phone, userPassword=password):

		user = getUser(phone=phone)

		exp = datetime.datetime.utcnow() + datetime.timedelta(days =0+days ,minutes=0+minutes)
		iat = datetime.datetime.utcnow()

		token_data = {'user':user.public_id, 'exp':exp, 'iat':iat}

		token = jwt.encode(token_data, current_app.config['SECRET_KEY'])

		result['data']['token'] = token.decode()
		result['status'] = status['success']
		return make_response(jsonify(result), 200)

	else:
		# wrong phone or password
		result['status'] = status['failure']
		result['message'] = 'wrong phone or password'
		return make_response(jsonify(result), 202)

@api.route('/logout', methods=['POST'])
def logoutUserRoute():
	pass

@api.route('/adduser', methods=['POST'])
@adminRequired
def addUserRoute():
	# the retuned response
	result = baseApi.copy()

	# get the post data
	post_data = request.get_json()
	
	userName = post_data.get('name')
	userPhone = post_data.get('phone')
	userPassword = post_data.get('password')
	userStatus = post_data.get('status')
	userPermission = post_data.get('permission')

	# this used to validate the phone number
	userCountryID = post_data.get('country_id')
	
	if not userPhone or not userPassword or not userCountryID:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# validate the password
	if not validatePassword(userPassword, MIN_PASSWORD_LENGTH):
		result['status'] = status['failure']
		result['message'] = 'Password not pass the validation'
		return make_response(jsonify(result), 400)

	# validate the phone number
	# ..
	# first git the country
	country = getCountry(id=userCountryID)
	if not country:
		result['status'] = status['failure']
		result['message']  = 'wrong country name'
		return make_response(jsonify(result), 400)
	# now validate
	userPhone = validatePhoneNumber(userPhone, country.phone_code, country.phone_length)
	if not userPhone:
		result['status'] = status['failure']
		result['message'] = 'phone number not pass the validation'
		return make_response(jsonify(result), 400)

	# make sure the user not already exists
	if getUser(phone=userPhone):
		result['status'] = status['failure']
		result['message'] = 'User already exists. Please Log in.'
		return make_response(jsonify(result), 202)

	if not addUser(name=userName, phone=userPhone, password=userPassword,\
				 status=userStatus, permission=userPermission):
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 201)

@api.route('/deleteuser', methods=['DELETE'])
def deleteUserRoute():
	pass

@api.route('/changeuserpermission', methods=['DELETE'])
@adminRequired
def changeUserPermissionRoute():
	pass


