""" tests the logic/person.py"""
from . import TestConfig
from app.logic.person import *

class TestUserLogic(TestConfig):
	""" tests the Person model operations """
	
	def test_addPerson(self):
		'''add new person'''

		result = addPerson(name='mustafa')

		person = Person.query.filter_by(name='mustafa').first()

		self.assertTrue(person)
		self.assertEqual(result, True, 'add person Failed')

	def test_addAge(self):
		'''add new age'''

		result = addAge(minAge=40, maxAge=50)

		age = Age.query.filter_by(min_age=40, max_age=50).first()

		self.assertTrue(age)
		self.assertEqual(result, True, 'add age Failed')

	def test_addPhoto(self):
		""" add new photo to a new person """

		link = r'https://losthuman.ru/assets/images/2018-09-22-formatirovanie-strok-v-python/top_image.jpg'

		addPerson(name='mustafa')

		person = Person.query.filter_by(name='mustafa').first()

		result = addPhoto(link=link, object=person)

		photo = Photos.query.filter_by(link=link).first()

		self.assertTrue(photo)
		self.assertEqual(result, True, 'add photo Failed')
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
