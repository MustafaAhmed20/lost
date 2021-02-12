from . import db
from . import datetime
from .user import Users


class Comment(db.Model):
	""" the comments under every operation"""
	__name__ = 'Comment'
	__tablename__ = 'comment'
	id = db.Column(db.Integer, primary_key=True)

	# the operation id 
	operation_id = db.Column(db.Integer,  db.ForeignKey('operations.id'), nullable=False)

	# the user who made the comment
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	# the date & time of the comment - UTC time
	time = db.Column(db.DATETIME(timezone=True), default=datetime.datetime.utcnow)

	# the text of the comment
	text = db.Column(db.TEXT)

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'operation_id':self.operation_id,
				'time':self.time.replace(tzinfo=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z'),
				'user':Users.query.get(self.user_id).toDict(),
				'text':self.text}

