from . import db
from ..extensions import datetime

class Feedback(db.Model):
	""" The feedback from the users"""

	__name__ = 'Feedback'
	__tablename__ = 'feedback'

	id = db.Column(db.Integer, primary_key=True)

	# date and time of add to the system
	add_date = db.Column(db.DATETIME, default=datetime.datetime.now())

	# the user created this operation
	user_public_id = db.Column(db.String(50))

	# the details (text) of the Feedback
	feedback = db.Column(db.TEXT)

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'date':self.add_date,
				'feedback':self.feedback, 'user_public_id':self.user_public_id}