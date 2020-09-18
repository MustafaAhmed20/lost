from . import db

from .person import Person
from .car import Car

class Accident(db.Model):
	""" The object-type 'accident'.
	accident involved persons and cars"""
	
	__name__ = 'Accident'
	__tablename__ = 'accident'
	id = db.Column(db.Integer, primary_key=True)

	# Cars involved in this accident
	cars = db.relationship("Car", backref="accident", cascade = "all, delete, delete-orphan")

	# Persons involved in this accident
	persons = db.relationship("Person", backref="accident", cascade = "all, delete, delete-orphan")

	def toDict():
		""" return dict representation of the object """
		return {'id':self.id, 'cars':[i.toDict() for i in self.cars], 'persons':[i.toDict() for i in self.persons]}
