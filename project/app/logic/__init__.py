"""This module will contain all the app logic as functions to be reusable."""
from .person import addPerson, deletePerson
from .car import addCar, deleteCar
from .accident import addAccident, deleteAccident

import json

# this contain the available objects types
availableObjectsTypes = ['Person', 'Car', 'Accident']

def addObject(objectName, post_data):
	# check if its valid object
	if objectName not in availableObjectsTypes:
		return False

	if objectName == availableObjectsTypes[0]:
		# person
		return _addObjectPerson(post_data)

	if objectName == availableObjectsTypes[1]:
		# car
		return _addObjectCar(post_data)
	
	if objectName == availableObjectsTypes[2]:
		# Accident
		return _addObjectAccident(post_data)

def deleteObject(objectName, object):
	# check if its valid object
	if objectName not in availableObjectsTypes:
		return False

	if objectName == availableObjectsTypes[0]:
		# person
		return _deleteObjectPerson(object)

	if objectName == availableObjectsTypes[1]:
		# car
		return _deleteObjectCar(object)

	if objectName == availableObjectsTypes[2]:
		# Accident
		return _deleteObjectAccident(object)


# helper functions to add objects
def _addObjectPerson(post_data):
	""" get the person data. return False if add person failed. 
		return the person object if added"""

	personName = post_data.get('person_name')
	gender = post_data.get('gender')
	skin = post_data.get('skin')
	age_id = post_data.get('age_id')

	if not age_id or not gender:
		return False

	# add person
	person = addPerson(name=personName, ageId=age_id, gender=gender, skin=skin)
	if not person:
		return False

	return person

def _addObjectCar(post_data):
	""" get the car data. return False if add car failed. 
		return the car object if added"""

	brand = post_data.get('brand')
	model = post_data.get('model')
	plateNumberLetters = post_data.get('plate_number_letters')
	plateNumberNumbers = post_data.get('plate_number_numbers')
	type = post_data.get('car_type')

	if not all([brand, model, plateNumberLetters, plateNumberNumbers, type]):
		return False

	# add car
	car = addCar(type=type, plateNumberLetters=plateNumberLetters, plateNumberNumbers=plateNumberNumbers, 
		brand=brand, model=model)
	
	if not car:
		return False

	return car

def _addObjectAccident(post_data):
	""" add the Accident data. return False if add Accident failed. 
		return the Accident object if added"""
	
	cars = post_data.get('cars')
	persons = post_data.get('persons')

	# the cars and persons must be lists of dicts
	if (cars and not type(cars) is str) or (persons and not type(persons) is str):
		return False
	
	# the Accident must include one person or one car at least
	if not cars and not persons:
		return False

	# initialize the list with None
	personObjects = None
	carObjects = None
	
	# add the cars
	if cars:
		# load the json object
		try:
			cars = json.loads(cars)
		except expression as e:
			return False
		carObjects = [_addObjectCar(i) for i in cars]
		
		# if one of the cars not added correctly return False after delete the added ones
		if not all(carObjects):
			# delete the objects
			for i in carObjects:
				if i:
					_deleteObjectCar(i)
			return False

	# add the persons
	if persons:
		# load the json object
		try:
			persons = json.loads(persons)
		except expression as e:
			return False
		personObjects = [_addObjectPerson(i) for i in persons]

		# if one of the persons not added correctly return False after delete the added ones
		if not all(personObjects):
			# delete the objects
			for i in personObjects:
				if i:
					_deleteObjectPerson(i)
			return False

	# now add the Accident
	return addAccident(cars =carObjects, persons =personObjects)

# helper functions to delete objects
def _deleteObjectPerson(object):
	''' delete object'''

	return deletePerson(object=object)

def _deleteObjectCar(object):
	''' delete object'''

	return deleteCar(object=object)

def _deleteObjectAccident(object):
	''' delete object'''

	return deleteAccident(object=object)