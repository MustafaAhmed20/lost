"""This module will contain all the app logic as functions to be reusable."""
from .person import addPerson, deletePerson

# this contain the available objects types
availableObjectsTypes = ['Person']

def addObject(objectName, post_data):
	# check if its valid object
	if objectName not in availableObjectsTypes:
		return False

	if objectName == availableObjectsTypes[0]:
		# person
		return _addObjectPerson(post_data)

def deleteObject(objectName, object):
	# check if its valid object
	if objectName not in availableObjectsTypes:
		return False

	if objectName == availableObjectsTypes[0]:
		# person
		return _deleteObjectPerson(object)


# helper functions to add objects
def _addObjectPerson(post_data):
	""" get the prson data. return False if add person failed. 
		return the person object if added"""
	personName = post_data.get('person_name')
	age_id = post_data.get('age_id')

	# add person
	person = addPerson(name=personName, ageId=age_id)
	if not person:
		return False

	return person

def _deleteObjectPerson(object):
	''' delete object'''

	return deletePerson(object=object)