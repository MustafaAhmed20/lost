""" tests the logic/person.py"""
from . import TestConfig
from app.logic.person import *

class TestUserLogic(TestConfig):
	""" tests the Person model operations """
	
	def test_addPerson(self):
		'''add new person'''

		result = addPerson(name='mustafa')

		person = Person.query.filter_by(name='mustafa').first()

		self.assertTrue(person, 'add person Failed')
		self.assertEqual(result.name, 'mustafa', 'add person Failed')

	def test_addAge(self):
		'''add new age'''

		result = addAge(minAge=40, maxAge=50)

		age = Age.query.filter_by(min_age=40, max_age=50).first()

		self.assertTrue(age, 'add age Failed')
		self.assertEqual(result.min_age, 40, 'add age Failed')

	def test_addPhoto(self):
		""" add new photo to a new person """

		link = r'https://losthuman.ru/assets/images/2018-09-22-formatirovanie-strok-v-python/top_image.jpg'

		addPerson(name='mustafa')

		person = Person.query.filter_by(name='mustafa').first()

		result = addPhoto(link=link, object=person)

		photo = Photos.query.filter_by(link=link).first()

		self.assertTrue(photo, 'add photo Failed')
		self.assertEqual(result.link, link, 'add photo Failed')
		self.assertEqual(photo.object, person, 'not the same person')
		self.assertEqual(photo.link, link, 'not the same link')

	def test_deletePerson(self):
		""" add new person and photos then delete them"""
		link = r'https://losthuman.ru/assets/images/2018-09-22-formatirovanie-strok-v-python/top_image.jpg'
		
		addPerson(name='mustafa')

		person = Person.query.filter_by(name='mustafa').first()

		# add 4 photos to person
		addPhoto(link=link, object=person)
		addPhoto(link=link, object=person)
		addPhoto(link=link, object=person)
		addPhoto(link=link, object=person)

		result = deletePerson(id=person.id)

		# try Search for the person
		personFinded = Person.query.filter_by(name='mustafa').first()

		photos = Photos.query.filter_by(link=link).all()
		photo = Photos.query.filter_by(link=link).first()

		self.assertEqual(result, True, 'delete photo Failed')
		self.assertEqual(personFinded, None, 'person not deleted')
		self.assertEqual(photos, [], 'photos not deleted')
		self.assertEqual(photo, None, 'photo not deleted')

class TestUserLogic2(TestConfig):
	""" tests the Person model operations """

	def test_getAge(self):
		""" get the Countries"""

		result = getAge()

		self.assertTrue(result, 'no Ages')
		

		result = getAge(minAge=1, maxAge=10)

		self.assertTrue(result, 'no age with this perm')
		self.assertEqual(result.min_age, 1)
		self.assertEqual(result.max_age, 10)

		result = getAge(id=1)

		self.assertTrue(result, 'no Age with id=1')
		self.assertEqual(result.id, 1)

	def test_getPhotos(self):
		""" add photos then find it"""

		link = 'this some link'
		object = addPerson(name='mustafa')

		newPhoto =  addPhoto(link=link, object=object)

		result = getPohto(id=newPhoto.id)

		self.assertTrue(result, 'no Photo')
		self.assertEqual(result.link, link)

		result = getPohto(object=object)

		self.assertTrue(result, 'no photo')
		self.assertEqual(result[0].object_id, object.id)

		result = getPohto()

		self.assertTrue(result, 'no photos')
