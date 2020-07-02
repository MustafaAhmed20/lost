""" tests the logic/person.py"""
from . import TestConfig
from app.logic.operation import *
from app.logic.user import Users
from app.logic.person import Person, addPerson



import datetime

class TestOperationLogic(TestConfig):
	""" tests the Operation model operations """

	def test_addCountry(self):
		'''add new Country'''

		result = addCountry(name='usa', phoneCode=1)

		country = Country.query.filter_by(name='usa').first()

		self.assertTrue(country, 'add new country Failed')
		self.assertEqual(result.name, 'usa', 'add new country Failed')

	def test_addStatus_operation(self):
		'''add new Status operation'''

		result = addStatus_operation(name='locked')

		status = Status_operation.query.filter_by(name='locked').first()

		self.assertTrue(status, 'add new status operation Failed')
		self.assertEqual(result.name, 'locked', 'add new status operation Failed')

	def test_addType_operation(self):
		'''add new Type operation'''

		result = addType_operation(name='test')

		type = Type_operation.query.filter_by(name='test').first()

		self.assertTrue(type, 'add new Type operation Failed')
		self.assertEqual(result.name, 'test', 'add new Type operation Failed')

	def test_addOperation(self):
		'''add new Type operation'''

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id

		# the object this operation point to
		addPerson(name='mustafa')
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='lost').first()
		status = Status_operation.query.filter_by(name='active').first()
		country = Country.query.first()

		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.datetime.now())

		operation = Operations.query.first()



		self.assertTrue(userPublicId)
		self.assertTrue(type)
		self.assertTrue(status)
		self.assertTrue(country)
		self.assertTrue(operation, 'add new operation Failed')
		
		
		# make sure the operation get right data
		self.assertEqual(operation.country.id, country.id,	"operation don't have the right country")
		self.assertEqual(operation.type.id, type.id, 		"operation don't have the right type")
		self.assertEqual(operation.status.id, status.id, 	"operation don't have the right status")
		self.assertEqual(operation.user.public_id, userPublicId, "operation don't have the right user")
		self.assertEqual(operation.object_id, person.id, 	"operation don't have the right object")

	def test_addOperation2(self):
		'''add new Type operation'''

		lat = 48.856613
		lng = 2.352222

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id

		# the object this operation point to
		addPerson(name='mustafa')
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='found').first()
		status = Status_operation.query.filter_by(name='closed').first()
		country = Country.query.first()

		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.datetime.now(), lat=lat, lng=lng)

		operation = Operations.query.first()



		self.assertTrue(userPublicId)
		self.assertTrue(type)
		self.assertTrue(status)
		self.assertTrue(country)
		self.assertTrue(operation)
		
		
		# make sure the operation get right data
		self.assertEqual(operation.country.id, country.id,	"operation don't have the right country")
		self.assertEqual(operation.type.id, type.id, 		"operation don't have the right type")
		self.assertEqual(operation.status.id, status.id, 	"operation don't have the right status")
		self.assertEqual(operation.user.public_id, userPublicId, "operation don't have the right user")
		self.assertEqual(operation.object_id, person.id, 	"operation don't have the right object")
		self.assertEqual(float(operation.lat), lat, 	"operation don't have the right lat")
		self.assertEqual(float(operation.lng), lng, 	"operation don't have the right lng")

class TestOperationLogic2(TestConfig):
	""" tests the Operation model operations """

	def test_getCountry(self):
		""" get the Countries"""

		result = getCountry()

		self.assertTrue(result, 'no Countries')
		

		result = getCountry(name='sudan')

		self.assertTrue(result, 'no Country sudan')
		self.assertEqual(result.name, 'sudan')

		result = getCountry(id=1)

		self.assertTrue(result, 'no Country with id=1')
		self.assertEqual(result.id, 1)
		
		result = getCountry(phoneCode=249)

		self.assertEqual(result.phone_code, 249)
		self.assertTrue(result, 'no Country with id=1')

	def test_getStatus_operation(self):
		""" get the Countries"""

		result = getStatus_operation()

		self.assertTrue(result, 'no Status_operation')
		

		result = getStatus_operation(name='active')

		self.assertTrue(result, 'no Status_operation active')
		self.assertEqual(result.name, 'active')

		result = getStatus_operation(id=1)

		self.assertEqual(result.id, 1)
		self.assertTrue(result, 'no Status_operation with id=1')

	def test_getType_operation(self):
		""" get the Countries"""

		result = getType_operation()

		self.assertTrue(result, 'no Type_operation')
		

		result = getType_operation(name='lost')

		self.assertTrue(result, 'no Type_operation lost')
		self.assertEqual(result.name, 'lost')


		result = getType_operation(id=1)
		
		self.assertEqual(result.id, 1)
		self.assertTrue(result, 'no Type_operation with id=1')
		
