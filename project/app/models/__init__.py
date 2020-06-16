from .. import SQLAlchemy

def init_app(app):
	#from flask_sqlalchemy import SQLAlchemy	
	db =  SQLAlchemy()
	db.init_app(app)