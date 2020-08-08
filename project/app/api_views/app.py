from . import api, current_app, jsonify, request, make_response, jwt
from . import status, baseApi, copy, adminRequired
from . import getUser, addFeedback, getFeedback, deleteFeedback

import os

@api.route('/checkconnection')
def checkConnectionRoute():

	# the returned response
	result = copy.deepcopy(baseApi)

	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/checkversion', methods=['POST'])
def checkVersionRoute():
	''' if supported version (build number)'''

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	version = post_data.get('version')

	supportedVersion  = os.getenv('version')

	if not version:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	try:
		if int(version) < int(supportedVersion):
			# must upgrade the app
			result['status'] = status['failure']
			result['message'] = 'this version not supported any more'
			return make_response(jsonify(result), 426)

	except Exception as e:
		result['status'] = status['failure']
		result['message'] = 'the version number must be integer'
		return make_response(jsonify(result), 400)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/getfeedback', methods=['POST'])
@adminRequired
def getfeedbackRoute():
	''' get the feedback - admin only
		this route use POST method becouse it may contain login data'''
	
	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()
	
	userPublicId = post_data.get('userid')

	# feedback made by one user
	if userPublicId:
		user = getUser(publicId=userPublicId)
		if not user :
			result['status'] = status['failure']
			result['message'] = 'no user found with this id!'
			return make_response(jsonify(result), 400)

	# get the feedback
	feedback = getFeedback(userPublicId=userPublicId)
	
	# success
	result['status'] = status['success']
	result['data']['feedback'] = [f.toDict() for f in feedback]
	return make_response(jsonify(result), 200)

@api.route('/deletefeedback', methods=['DELETE'])
@adminRequired
def deletefeedbackRoute():
	''' delete a feedback by id or user_id'''

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	userPublicId = post_data.get('userid')
	feedbackId = post_data.get('feedbackid')

	if not userPublicId and not feedbackId:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# make sure a valid user public id
	if userPublicId:
		user = getUser(publicId=userPublicId)
		if not user:
			result['status'] = status['failure']
			result['message'] = 'no user found with this id!'
			return make_response(jsonify(result), 400)

	resultFeedback = deleteFeedback(userPublicId=userPublicId, id=feedbackId)

	if not resultFeedback:
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 200)

@api.route('/addfeedback', methods=['POST'])
def addFeedbackRoute():
	

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

	feedback = post_data.get('feedback')

	# required data
	if not feedback:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# if logged-in get the user id
	userPublicId = None

	# the user
	token = request.headers.get('token')
	if token:
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

	resultFeedback = addFeedback(text=feedback, userPublicId=userPublicId)

	if not resultFeedback:
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 201)
