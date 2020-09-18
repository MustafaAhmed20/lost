from ..models import db, Accident
from .person import deletePhoto


# accident model
def addAccident(cars =[], persons =[]):
	''' add new Accident - return Accident object if success else False
	perm: cars    = a List of car object
	perm: persons = a List of person object'''

	if not cars and not persons:
		# must be one person or one car at least
		return None
	
	try:
		accident = Accident()
		# add the cars and the persons	
		accident.cars.extend(cars)
		accident.persons.extend(persons)
		
		db.session.add(accident)
		db.session.commit()
	except Exception as e:
		return False

	return accident

def getAccident(id=None):
	""" return the Accident object or None if not exist
		return a list of all Accident if no id passed.
		return one object if filtered by 'id'"""

	if id:
		return Accident.query.get(id)

	
	return Accident.query.all()

def deleteAccident(id=None, object=None):
	""" delete the photos then delete the Accident
		perm : object = the Accident object"""

	if id:
		accident = Accident.query.get(id)
	elif object:
		accident = object

	if not accident:
		return False

	# delete the photos
	deletePhoto(accident)

	# delete the person
	db.session.delete(accident)

	db.session.commit()	

	return True
