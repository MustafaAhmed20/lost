from ..extensions import SQLAlchemy
from ..extensions import datetime

db =  SQLAlchemy()

def init_app(app):
	db.init_app(app)