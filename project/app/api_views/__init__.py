"""This module will contain the api 'Blueprint' and its views."""

from flask import Blueprint, current_app, jsonify, request, make_response
import json

# import the logic
from ..logic.user import *

# the login token valid time
minutes = 30
days = 1

api = Blueprint('api', __name__)

baseApi = {'status':None, 'message':None, 'data':{}}
status = {'failure':'failure', 'success':'success'}

from .user import *
