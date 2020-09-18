""" tests the logic/accident.py"""

from . import TestConfig
from app.logic.accident import *
from app.models import Accident, Person, Car

# cars and persons logic
from app.logic.person import addPerson
from app.logic.car import addCar

class TestAaccidentLogic(TestConfig):
	
	def test_addAccident(self):
		''' test add Accident functionality'''

		# first add car object
		car = addCar(type=1, plateNumberLetters='dfg', plateNumberNumbers='234', brand='test', model='test')
		self.assertTrue(car, 'add car failed')

		# now add the Accident
		accident = addAccident(cars=[car])
		self.assertTrue(accident, 'add accident failed')

		# check the new object in the databas
		result = Accident.query.all()

		self.assertTrue(result)
		self.assertEqual(len(result), 1, 'wrong length of accident objects')
	
	def test_addAccident2(self):
		''' test add Accident functionality'''

		# first add 2 car object
		car1 = addCar(type=1, plateNumberLetters='dfg', plateNumberNumbers='234', brand='test', model='test')
		car2 = addCar(type=3, plateNumberLetters='fgg', plateNumberNumbers='254', brand='test', model='test')
		self.assertTrue(car1, 'add car failed')
		self.assertTrue(car2, 'add car failed')

		# now add 1 persons object
		person = addPerson(name='test', gender='male', ageId=2, skin=3)
		
		self.assertTrue(person, 'add person failed')
		

		# now add the Accident
		accident = addAccident(cars=[car1, car2], persons=[person])
		self.assertTrue(accident, 'add accident failed')

		# check the new object in the databas
		result = Accident.query.all()

		self.assertTrue(result)
		self.assertEqual(len(result), 1, 'wrong length of accident objects')
		self.assertEqual(len(result[0].cars), 2, 'wrong length of cars objects')
		self.assertEqual(len(result[0].persons), 1, 'wrong length of person objects')
	
	def test_getAccident(self):
		''' add Accident then get it with getters'''
	
		# first add car object
		car = addCar(type=1, plateNumberLetters='dfg', plateNumberNumbers='234', brand='test', model='test')
		self.assertTrue(car, 'add car failed')

		# now add the Accident
		accident = addAccident(cars=[car])
		self.assertTrue(accident, 'add accident failed')

		# get the Accident with the getters func
		result = getAccident()
		self.assertTrue(result)
		self.assertEqual(len(result), 1, 'wrong length of Accident objects')

		id = result[0].id

		# filter with id
		result = getAccident(id=id)
		self.assertTrue(result)
		self.assertEqual(result.id, id)
		self.assertEqual(result.cars[0].brand, car.brand)

	def test_deleteAccident(self):
		''' add Accident then delete it'''

		# first add car object
		car = addCar(type=1, plateNumberLetters='dfg', plateNumberNumbers='234', brand='test', model='test')
		self.assertTrue(car, 'add car failed')

		# now add 1 persons object
		person = addPerson(name='test', gender='male', ageId=2, skin=3)

		# now add the Accident
		accident = addAccident(cars=[car], persons=[person])
		self.assertTrue(accident, 'add accident failed')

		# check the new object in the databas
		result = Accident.query.all()

		self.assertTrue(result)
		self.assertEqual(len(result), 1, 'wrong length of accident objects')

		# now delete it 
		result = deleteAccident(object=accident)
		self.assertTrue(result)

		# check the database again
		result = Accident.query.all()
		self.assertFalse(result)

		# check the persons and the cars associated with it(must be deleted)
		result = Car.query.all()
		self.assertFalse(result, 'car object did not get deleted')
		
		result = Person.query.all()
		self.assertFalse(result, 'person object did not get deleted')

