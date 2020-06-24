from ..models import db, Person, Age, Photos

# person model
def addPerson(name):
	""" add new Person """
	try:
		person = Person(name=name)
		db.session.add(person)
		db.session.commit()
	except Exception as e:
		return False

	return True

def deletePerson(id):
	""" delete the photos then delete the person"""

	person = Person.query.get(id)
	if not Person:
		return False

	photos = Photos.query.filter(Photos.object.is_type(Person)).all()

	# delete the photos
	for photo in photos:
		db.session.delete(photo)

	# delete the person
	db.session.delete(person)	

	return True

# Age model
def addAge(minAge, maxAge):

	try:
		age = Age(min_age=minAge, max_age=maxAge)
		db.session.add(age)
		db.session.commit()
	except Exception as e:
		return False

	return True

# Photos model
def addPhoto(link, object):
	""" add new photo
		perm: link = the link to the photo
		perm: object = the object this photo Belongs to as Model object"""
	try:
		photo = Photos(link=link, object=object)
		db.session.add(photo)
		db.session.commit()
	except Exception as e:
		return False

	return True
