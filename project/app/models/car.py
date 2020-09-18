from . import db

class Car(db.Model):
	""" The object-type 'Car'"""

	__name__ = 'Car'
	__tablename__ = 'car'

	id = db.Column(db.Integer, primary_key=True)

	# the type of the car (large - small) - range (1-5)
	type = db.Column(db.Integer)

	# Plate Number of the car (numbers - letters)
	plate_number = db.Column(db.String(10), unique=True)

	# car Brand
	brand = db.Column(db.TEXT)

	# car model
	model = db.Column(db.TEXT)

	# if this car involved in an  accident - access by accident
	accident_id = db.Column(db.Integer, db.ForeignKey('accident.id'))
	

	def toDict(self):
		""" return dict representation of the object """
		return {'id':self.id, 'type':self.type, 'brand':self.brand,'model':self.model,
		'plate_number_letters':self.plate_number.split('-')[0], 'plate_number_numbers':self.plate_number.split('-')[1]}
