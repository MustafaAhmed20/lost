from . import api, current_app, jsonify, request, make_response, jwt
from . import status, baseApi, copy, loginActiveRequired

# the comments logic
from . import addComment, getComment

@api.route('/getcomment', methods=['GET'])
def getCommentRoute():
	''' get the comments'''

	# the returned response
	result = copy.deepcopy(baseApi)

	# the filters
	filters = request.args

	if not filters:
		# no filters
		try:
			comments = getComment()
		except Exception as e:
			result['status'] = status['failure']
			result['message'] = 'Some error occurred. Please try again'
			return make_response(jsonify(result), 401)

		# success
		result['status'] = status['success']
		result['data']['comments'] = [comment.toDict() for comment in comments]
		return make_response(jsonify(result), 200)

	# filter by operation id
	operationId = filters.get('operationid')
	userPublicId = filters.get('user')
	comments = []

	if operationId:
		comments = getComment(operationId=operationId)
	elif userPublicId:
		user = getUser(userPublicId=userPublicId)
		if user:
			comments = getComment(userId=user.id)

	# success
	result['status'] = status['success']
	result['data']['comments'] = [comment.toDict() for comment in comments]
	return make_response(jsonify(result), 200)

@api.route('/sendcomment', methods=['POST'])
@loginActiveRequired
def sendCommentRoute():
	''' the user make a comment on some ad (operation)'''

	# the returned response
	result = copy.deepcopy(baseApi)

	# get the post data
	post_data = request.get_json()

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

	text = post_data.get('text')
	operationId = post_data.get('operationid')
	
	# required data
	if not text or not operationId:
		result['status'] = status['failure']
		result['message'] = 'required data not submitted'
		return make_response(jsonify(result), 400)

	# save the comment in the DB
	resultComment = addComment(text=text, userPublicId=userPublicId, operationId=operationId)

	if not resultComment:
		result['status'] = status['failure']
		result['message'] = 'Some error occurred. Please try again'
		return make_response(jsonify(result), 401)

	# success
	result['status'] = status['success']
	return make_response(jsonify(result), 201)

