from . import api, current_app, jsonify, request, make_response, json
from . import days, minutes, status, baseApi, copy
from . import adminRequired, loginRequired
from ..extensions import jwt
import datetime

# the logic
from . import (login, getUser, addUser, getCountry, validatePassword, validatePhoneNumber, 
				registerUser, VerifyUser, forgotPassword, resetPassword, updateUserData,
				getPermission, getStatus)

# the shortest length for passwords
MIN_PASSWORD_LENGTH = 5

@api.route('/login', methods=['POST'])
def loginUserRoute():
	result = copy.deepcopy(baseApi)

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
		# generate token
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

@api.route('/checklogin', methods=['POST'])
@loginRequired
def checkLoginRoute():
	''' this route just for checking the token if valid or not'''
	result = copy.deepcopy(baseApi)
	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/logout', methods=['POST'])
def logoutUserRoute():
	pass

@api.route('/adduser', methods=['POST'])
@adminRequired
def addUserRoute():
	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()
	
	userName = post_data.get('name')
	userPhone = post_data.get('phone')
	userPassword = post_data.get('password')
	userStatus = post_data.get('status')
	userPermission = post_data.get('permission')

	# this used to validate the phone number
	userCountryID = post_data.get('country_id')
	
	if not userPhone or not userPassword or not userCountryID or not userName:
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

@api.route('/modifyuser', methods=['PUT'])
@loginRequired
def modifyUserRoute():
	# modify the user data with the user him self logged-in

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	userName = post_data.get('name')

	# if the user want change the password - must sumbit the old password
	userPassword = post_data.get('password')
	userNewPassword = post_data.get('newpassword')

	if userNewPassword:
		# submit the old password
		if not userPassword:
			result['status'] = status['failure']
			result['message'] = 'required data not submitted'
			return make_response(jsonify(result), 400)

		# validate the old/new passwords
		if not validatePassword(userPassword, MIN_PASSWORD_LENGTH) or not validatePassword(userNewPassword, MIN_PASSWORD_LENGTH):
			result['status'] = status['failure']
			result['message'] = 'Password not pass the validation'
			return make_response(jsonify(result), 400)


	# get the user
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

	user = getUser(publicId=userPublicId)

	# update the data
	updateResult = updateUserData(user=user, name=userName, newPassword=userNewPassword, password=userPassword)

	if not updateResult:
		result['status'] = status['failure']
		result['message']  = 'update data Failed'
		return make_response(jsonify(result), 202)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/changeuserpermission', methods=['DELETE'])
@adminRequired
def changeUserPermissionRoute():
	pass

@api.route('/registeruser', methods=['POST'])
def registerUserRoute():
	""" register user with sms Verification"""

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()
	
	userName = post_data.get('name')
	userPhone = post_data.get('phone')
	userPassword = post_data.get('password')

	# this used to validate the phone number
	userCountryID = post_data.get('country_id')
	
	if not userPhone or not userPassword or not userCountryID :
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

	# user, code
	userAndCode = registerUser(phone=userPhone, password=userPassword, name=userName)

	if not userAndCode:
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	user, code = userAndCode

	# send the sms to the user
	#

	# login the new user by giving him a token
	# generate token
	exp = datetime.datetime.utcnow() + datetime.timedelta(days =0+days ,minutes=0+minutes)
	iat = datetime.datetime.utcnow()

	token_data = {'user':user.public_id, 'exp':exp, 'iat':iat}

	token = jwt.encode(token_data, current_app.config['SECRET_KEY'])

	# success
	result['status'] = status['success']
	result['data']['token'] = token.decode()
	return make_response(jsonify(result), 201)

@api.route('/conformuserphone', methods=['POST'])
@loginRequired
def conformUserPhoneRoute():
	''' conform the user phone with code sended to him'''

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	conformCode = post_data.get('code')
	
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

	if not conformCode :
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# conform the user
	conformResult = VerifyUser(code=conformCode, userPublicId=userPublicId)

	if not conformResult:
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/forgotpassword', methods=['POST'])
def forgotPasswordRoute():
	""" send sms Verification code to user"""

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()
	
	# user phone
	userPhone = post_data.get('phone')
	
	# this used to validate the phone number
	userCountryID = post_data.get('country_id')

	if not userPhone or not userCountryID :
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
	userPhone = validatePhoneNumber(userPhone, country.phone_code, country.phone_length)
	if not userPhone:
		result['status'] = status['failure']
		result['message'] = 'phone number not pass the validation'
		return make_response(jsonify(result), 400)

	# get a new code if the phone is valid user-phone
	codeObject = forgotPassword(phone=userPhone)

	if not codeObject:
		# no user with this phone
		result['status'] = status['failure']
		result['message'] = 'no user with this phone'
		return make_response(jsonify(result), 202)

	# send the sms to the user
	#

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/resetpassword', methods=['POST'])
def resetPasswordRoute():
	''' rest the password for a user if submitted valid Verification code '''

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()
	
	# user phone
	userPhone = post_data.get('phone')
	code = post_data.get('code')
	password = post_data.get('password')
	
	# this used to validate the phone number
	userCountryID = post_data.get('country_id')

	if not userPhone or not userCountryID or not code:
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
	userPhone = validatePhoneNumber(userPhone, country.phone_code, country.phone_length)
	if not userPhone:
		result['status'] = status['failure']
		result['message'] = 'phone number not pass the validation'
		return make_response(jsonify(result), 400)

	if not password:
		# this mean only validate the code withot reset the password
		
		success =  resetPassword(code=code, phone=userPhone)

		if not success:
			# the code not valid
			result['status'] = status['failure']
			result['message']  ='Invalid code.'
			return make_response(jsonify(result), 202)
		
		else:
			# success
			result['status'] = status['success']
			return make_response(jsonify(result), 200)



	else:
		# check the code then reset the password and delete the code


		# first validate the password
		if not validatePassword(password, MIN_PASSWORD_LENGTH):
			result['status'] = status['failure']
			result['message'] = 'Password not pass the validation'
			return make_response(jsonify(result), 400)

		# now the check the code and change the password
		success =  resetPassword(code=code, phone=userPhone, newPassword=password)

		if not success:
			# the code not valid
			result['status'] = status['failure']
			result['message']  ='Invalid code.'
			return make_response(jsonify(result), 202)
		
		else:
			# success - password reseted
			result['status'] = status['success']
			return make_response(jsonify(result), 200)

@api.route('/getuser', methods=['POST'])
def getUserRoute():
	''' this route use 'POST' method because it contain sensitive data
		get the user data with phone or public id '''

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	# user phone
	userPhone = post_data.get('phone')
	userPublicId = post_data.get('userid')

	if not userPhone and not userPublicId:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	if userPublicId:
		user = getUser(publicId=userPublicId)

	if userPhone:
		user = getUser(phone=userPhone)

	if not user:
		result['status'] = status['success']
		result['data']['user'] = []
		return make_response(jsonify(result), 200)

	# success
	result['status'] = status['success']
	result['data']['user'] = [user.toDict()]
	return make_response(jsonify(result), 200)


##
##
# Permission & Status
@api.route('/getpermission')
def getPermissionRoute():
	""" Return a list of available user permissions"""

	# the returned response
	result = copy.deepcopy(baseApi)

	permissions = getPermission()

	result['status'] = status['success']
	result['data']['permission'] = [p.toDict() for p in permissions]
	return make_response(jsonify(result), 200)

@api.route('/getstatus')
def getStatusRoute():
	""" Return a list of available user permissions"""

	# the returned response
	result = copy.deepcopy(baseApi)

	userStatus = getStatus()

	result['status'] = status['success']
	result['data']['status'] = [s.toDict() for s in userStatus]
	return make_response(jsonify(result), 200)

