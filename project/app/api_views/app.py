from . import api, current_app, jsonify, request, make_response
from . import status, baseApi

@api.route('/checkconnection')
def checkConnectionRoute():

	# the returned response
	result = baseApi.copy()

	result['status'] = status['success']
	return make_response(jsonify(result), 200)

