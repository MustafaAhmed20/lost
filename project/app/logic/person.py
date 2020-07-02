from ..models import db, Person, Age, Photos

# person model
def addPerson(name, ageId=None):
	""" add new Person 
	return the new person object if added or false if failed"""
	try:
		person = Person(name=name)

		if ageId:
			age = Age.query.get(ageId)
			if age:
				age.persons.append(person)

		db.session.add(person)
		db.session.commit()
	except Exception as e:
		return False

	return person

def getPerson(id=None):
	""" return the age object or None if not exist
		return a list of all ages if no id passed."""

	if not id:
		return Person.query.all()

	if id:
		return Age.query.get(id)

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
	"""return the new age object if added or false if failed """
	
	try:
		age = Age(min_age=minAge, max_age=maxAge)
		db.session.add(age)
		db.session.commit()
	except Exception as e:
		return False

	return age

def getAge(id=None, minAge=None, maxAge=None):
	""" return the age object or None if not exist
		return a list of all ages if no id passed."""

	if not any([id, minAge, maxAge]):
		return Age.query.all()

	if id:
		return Age.query.get(id)
	elif all([minAge, maxAge]):
		return Age.query.filter_by(min_age=minAge, max_age=maxAge).first()
	else:
		return None
		

# Photos model
def addPhoto(link, object):
	""" add new photo
		perm: link = the link to the photo
		perm: object = the object this photo Belongs to as Model object

		return the new photo object if added or false if failed"""
	try:
		photo = Photos(link=link, object=object)
		db.session.add(photo)
		db.session.commit()
	except Exception as e:
		return False

	return photo
