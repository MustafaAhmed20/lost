from .. import SQLAlchemy
import datetime

db =  SQLAlchemy()

def init_app(app):
	db.init_app(app)