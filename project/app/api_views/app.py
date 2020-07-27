from . import api, current_app, jsonify, request, make_response
from . import status, baseApi, copy

@api.route('/checkconnection')
def checkConnectionRoute():

	# the returned response
	result = copy.deepcopy(baseApi)

	result['status'] = status['success']
	return make_response(jsonify(result), 200)

