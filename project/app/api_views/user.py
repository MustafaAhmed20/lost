from . import api, current_app, jsonify, request, make_response, json
from . import days, minutes, status, baseApi
from ..extensions import jwt
import datetime

# the logic
from . import login, getUser

@api.route('/login', methods=['POST'])
def loginUser():
	result = baseApi.copy()

	# get the post data
	post_data = request.get_json()
	try:
		phone = post_data.get('phone')
		password = post_data.get('password')
	except Exception as e:

		result['status'] = status['failure']
		baseApi['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	if not phone or not password:
		result['status'] = status['failure']
		baseApi['message'] = 'required data not submitted'
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
		return make_response(jsonify(result), 401)

@api.route('/logout', methods=['POST'])
def logoutUser():
	pass

@api.route('/adduser', methods=['POST'])
def addUser():
	pass

@api.route('/deleteuser', methods=['DELETE'])
def deleteUser():
	pass

@api.route('/changeuserpermission', methods=['DELETE'])
def changeUserPermission():
	pass


