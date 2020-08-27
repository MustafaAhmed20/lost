"""This module will contain all the app logic as functions to be reusable."""
from .person import addPerson, deletePerson
from .car import addCar, deleteCar

# this contain the available objects types
availableObjectsTypes = ['Person', 'Car']

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


# helper functions to add objects
def _addObjectPerson(post_data):
	""" get the prson data. return False if add person failed. 
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
	plateNumberNunbers = post_data.get('plate_number_numbers')
	type = post_data.get('car_type')

	if not all([brand, model, plateNumberLetters, plateNumberNunbers, type]):
		return False

	# add car
	car = addCar(type=type, plateNumberLetters=plateNumberLetters, plateNumberNumbers=plateNumberNunbers, 
		brand=brand, model=model)
	
	if not car:
		return False

	return car


# helper functions to delete objects
def _deleteObjectPerson(object):
	''' delete object'''

	return deletePerson(object=object)

def _deleteObjectCar(object):
	''' delete object'''

	return deleteCar(object=object)
