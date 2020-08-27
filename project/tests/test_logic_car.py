""" tests the logic/car.py"""
from . import TestConfig
from app.logic.car import *

class TestAppLogic(TestConfig):
	def test_addCar(self):
		''' add new car'''

		result = addCar(type=1, plateNumberLetters='lsd', plateNumberNumbers='231', brand='brand', model='toyota')
		self.assertTrue(result, 'add car failed')

		# check the car in the database
		car = Car.query.filter_by(model='toyota').first()
		self.assertTrue(car, 'no car Found')

	def test_addCar2(self):
		''' add new car the get it with filters'''

		result = addCar(type=1, plateNumberLetters='lsd', plateNumberNumbers='231', brand='brand', model='toyota')
		self.assertTrue(result, 'add car failed')

		# get the car
		car = getCar(plateNumberLetters='lsd', plateNumberNumbers='231')
		self.assertTrue(car, 'no car Found')
		self.assertEqual(car.model, 'toyota', 'not the same car data')

		# filter with type
		# Note filter with type return a list
		cars = getCar(type=1)
		self.assertTrue(cars[0])
		self.assertEqual(cars[0].model, 'toyota', 'not the same car data')

