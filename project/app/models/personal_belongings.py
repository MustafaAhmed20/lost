from . import db

class PersonalBelongings(db.Model):
	__name__ = 'PersonalBelongings'
	__tablename__ = 'personal_belongings'

	id = db.Column(db.Integer, primary_key=True)

	# Personal belongings type
	type = db.Column(db.Integer, nullable=False)

	# some types have subtype
	subtype = db.Column(db.Integer, nullable=False)

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'type':self.type, 'subtype':self.subtype}