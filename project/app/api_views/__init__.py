"""This module will contain the api 'Blueprint' and its views."""

from flask import Blueprint


api = Blueprint('api', __name__)

@api.route("/")
def test():
	return 'this api route'