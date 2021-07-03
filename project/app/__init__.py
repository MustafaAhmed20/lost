from flask import Flask, make_response
from .extensions import load_dotenv

import os

def create_app():
	# load the variables from the env file!
	thisPath:str = os.path.abspath(os.path.dirname(__file__))

	envPath:str = os.path.abspath(os.path.join(thisPath, os.pardir))

	dotenv_path = os.path.join(envPath, '.env')
	
	load_dotenv(dotenv_path=dotenv_path)

	from . import models, api_views #, services
	app = Flask(__name__)

	# Configurations
	app.config.from_object('config')

	# create the app with static file serve the imeges
	app.static_url_path = 'static/imeges'
	
	models.db.init_app(app)

	# register the blueprints
	app.register_blueprint(api_views.api, url_prefix='/api')
	app.register_blueprint(api_views.api, url_prefix='/beta')
	
	return app

fullApp = create_app()