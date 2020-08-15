"""This module will contain the api 'Blueprint' and its views."""

from flask import Blueprint, current_app, jsonify, request, make_response
import json, os
import datetime 
from functools import wraps
from ..extensions import secure_filename
import copy


# import the logic
from ..logic.user import *
from ..logic.person import *
from ..logic.operation import *
from ..logic.app import *

# the login token valid time
minutes = 30
days = 1

api = Blueprint('api', __name__)

baseApi = {'status':None, 'message':None, 'data':{}}
status = {'failure':'failure', 'success':'success'}

MAX_IMEGES_NUMBER = 5
ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']

def adminRequired(f):
	@wraps(f)
	def mustAdmin(*args, **kwargs):
		
		# get the tkoken
		token = request.headers.get('token')
		result = copy.deepcopy(baseApi)
		
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
		result = copy.deepcopy(baseApi)
		
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

def loginActiveRequired(f):
	""" the user must be with Active status """
	@wraps(f)
	def mustlogin(*args, **kwargs):
		# get the tkoken
		token = request.headers.get('token')
		result = copy.deepcopy(baseApi)
		
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

		user = getUser(publicId = userPublicId)
		availableStatus = getStatus(name='active')

		if availableStatus:
			if user not in availableStatus.users:
				result['status'] = status['failure']
				result['message']  ='This user not active.'
				return make_response(jsonify(result), 202)
		else:
			result['status'] = status['failure']
			result['message']  ='Some error occurred. Please try again'
			return make_response(jsonify(result), 401)


		# success
		return f(*args, **kwargs)

	return mustlogin

def saveFile(file):
	''' take file and save it, return link to the photo'''
	filename = file.filename
	if not filename:
		return False
	try:
		ext = file.filename.split('.')[-1]
		if ext.lower() not in ALLOWED_EXTENSIONS:
			return False
			

		filename = filename.split('.')[0] + str(datetime.datetime.now()) + '.' + ext
		filename = secure_filename(filename)
		path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
		file.save(path)

		#return path
		return f'static/imeges/{filename}'

	except Exception as e:
		
		return False

	
from .user import *
from .person import *
from .operation import *
from .app import *
