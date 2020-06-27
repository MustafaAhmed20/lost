"""This module will contain the api 'Blueprint' and its views."""

from flask import Blueprint, current_app, jsonify, request, make_response
import json

from functools import wraps

# import the logic
from ..logic.user import *

# the login token valid time
minutes = 30
days = 1

api = Blueprint('api', __name__)

baseApi = {'status':None, 'message':None, 'data':{}}
status = {'failure':'failure', 'success':'success'}

def adminRequired(f):
	@wraps(f)
	def mustAdmin(*args, **kwargs):
		
		# get the tkoken
		token = request.headers.get('token')
		result = baseApi.copy()
		
		if not token:
			result['status'] = status['failure']
			result['message'] = 'token required!'
			make_response(jsonify(result), 400)

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

		if not user:
			result['status'] = status['failure']
			result['message']  ="Please log in again."
			return make_response(jsonify(result), 202)

		if not user.permission.name == 'admin':
			result['status'] = status['failure']
			result['message']  ="You don't have the permission."
			return make_response(jsonify(result), 401)

		# success
		return f(*args, **kwargs)

	return mustAdmin

def loginRequired(f):
	@wraps(f)
	def mustlogin(*args, **kwargs):
		# get the tkoken
		token = request.headers.get('token')
		result = baseApi.copy()
		
		if not token:
			result['status'] = status['failure']
			result['message'] = 'token required!'
			make_response(jsonify(result), 400)

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

		

		# success
		return f(*args, **kwargs)

	return mustlogin

from .user import *
