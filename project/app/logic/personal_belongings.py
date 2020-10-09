from ..models import db, PersonalBelongings
from .person import deletePhoto

# PersonalBelongings model
def addPersonalBelongings(type, subtype):
	''' add new PersonalBelongings - return PersonalBelongings object if success else False'''

	try:
		object = PersonalBelongings(type=type, subtype=subtype)
		db.session.add(object)
		db.session.commit()
	except expression as identifier:
		return False

	return object

def getPersonalBelongings(id=None, type=None, subtype=None):
	""" return the PersonalBelongings object or None if not exist
		return a list of all PersonalBelongings if no filters passed.
		return one object if filtered by 'id'"""

	# filter with id
	if id:
		return PersonalBelongings.query.get(id)

	if type:
		# NOTICE: query by subtype only work if filter by type also
		query = PersonalBelongings.query.filter_by(type=type)
		if subtype:
			query = query.filter_by(subtype=subtype)
		
		return query.all()

	# all the data
	return PersonalBelongings.query.all()

def deletePersonalBelongings(id=None, object=None):
	""" delete the photos then delete the 'PersonalBelongings'
		perm : object = the 'PersonalBelongings' object"""

	
	if id:
		targerObject = PersonalBelongings.query.get(id)
	elif object:
		targerObject = object

	if not targerObject:
		return False

	# delete the photos
	deletePhoto(targerObject)

	# delete the PersonalBelongings
	db.session.delete(targerObject)

	db.session.commit()	

	return True
