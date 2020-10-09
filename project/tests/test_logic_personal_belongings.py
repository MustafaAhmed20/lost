""" tests the logic/personal_belongings.py"""
from . import TestConfig
from app.logic.personal_belongings import *

class TestPersonalBelongingsLogic(TestConfig):
	""" tests the 'PersonalBelongings' model operations """

	def test_PersonalBelongings(self):
		''' test add 'PersonalBelongings' functionality'''

		result = addPersonalBelongings(type=1, subtype=2)

		p = PersonalBelongings.query.first()

		self.assertTrue(p, 'no object added')
		self.assertTrue(result, 'no object added')

		self.assertEqual(p.type, 1, 'not same type')
		self.assertEqual(p.subtype, 2, 'not same subtype')

		# get the object with the getter

		# witout filter
		result = getPersonalBelongings()

		self.assertTrue(result, 'no data returned')
		self.assertEqual(len(result), 1, 'wrong length of objects')

		# filter with id
		result = getPersonalBelongings(id=p.id)
		self.assertTrue(result, 'no data returned')

		# not found - wrong id
		result = getPersonalBelongings(id=p.id+1)
		self.assertFalse(result, 'data returned')

		# filter with type
		result = getPersonalBelongings(type=1)
		self.assertTrue(result, 'no data returned')
		self.assertEqual(len(result), 1, 'wrong length of objects')

		# filter with type and subtype
		result = getPersonalBelongings(type=1, subtype=2)
		self.assertTrue(result, 'no data returned')
		self.assertEqual(len(result), 1, 'wrong length of objects')

		# wrong type - not Found
		result = getPersonalBelongings(type=2)
		self.assertFalse(result, 'data returned')

		# wrong subtype
		result = getPersonalBelongings(type=1, subtype=3)
		self.assertFalse(result, 'data returned')

		# now delete the object
		#

		result = deletePersonalBelongings(object=p)
		self.assertTrue(result)

		# now check the database again
		p = PersonalBelongings.query.first()

		self.assertFalse(p, 'data returned')
