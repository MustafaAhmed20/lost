from ..models import db, Person, Age, Photos
import os

# person model
def addPerson(name, gender, ageId, skin=None, shelter=False):
	""" add new Person 
	return the new person object if added or false if failed"""

	if gender not in ('male', 'female'):
		raise ValueError('not valid gender')
	if gender == 'male':
		gender = True
	else:
		gender = False

	try:
		person = Person(name=name, gender=gender, skin=skin, shelter=shelter)

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
	""" return the Person object or None if not exist
		return a list of all Persons if no id passed."""

	if not id:
		return Person.query.all()

	if id:
		return Person.query.get(id)

def deletePerson(id=None, object=None):
	""" delete the photos then delete the person
		perm : object = the person object"""

	if id:
		person = Person.query.get(id)
	elif object:
		person = object

	if not person:
		return False

	# delete the photos
	deletePhoto(person)

	# delete the person
	db.session.delete(person)

	db.session.commit()	

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
def addPhoto(link, fullPath,object):
	""" add new photo
		perm: link = the link to the photo
		perm: object = the object this photo Belongs to as Model object

		return the new photo object if added or false if failed"""
	try:
		photo = Photos(link=link, full_path=fullPath ,object=object)
		db.session.add(photo)
		db.session.commit()
	except Exception as e:
		return False

	return photo

def getPohto(id=None, object=None):
	""" return the photo object or None if not exist
		return a list of all ages if no id passed."""

	if not any([id, object]):
		return Photos.query.all()

	if id:
		return Photos.query.get(id)

	if object:
		return Photos.query.filter_by(object=object).all()

def deletePhoto(object):
	''' delete photo from the system
		perm: object that connected to photos'''
	photos = Photos.query.filter_by(object=object).all()

	# delete the photos from the system
	for photo in photos:
		try:
			os.remove(photo.full_path)
		except Exception as e:
			pass

	# delete the photos from db
	for photo in photos:
		db.session.delete(photo)
	db.session.commit()

	return True
