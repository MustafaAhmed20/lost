from flask import Flask, make_response
from .extensions import load_dotenv

def create_app():
	# load the variables from the env file!
	load_dotenv()

	from . import models, api_views #, services
	app = Flask(__name__)

	# Configurations
	app.config.from_object('config')

	# create the app with static file serve the imeges
	app.static_url_path = 'static/imeges'
	
	models.db.init_app(app)

	# register the blueprints
	app.register_blueprint(api_views.api, url_prefix='/api')
	
	#routes.init_app(app)
	#services.init_app(app)
	return app

fullApp = create_app()