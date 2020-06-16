from flask import Flask
from flask_sqlalchemy import SQLAlchemy	

from dotenv import load_dotenv

def create_app():
	# load the variables from the env file!
	load_dotenv()

	from . import models #, routes, services
	app = Flask(__name__)

	# Configurations
	app.config.from_object('config')

	models.init_app(app)
	#routes.init_app(app)
	#services.init_app(app)
	return app

fullApp = create_app()