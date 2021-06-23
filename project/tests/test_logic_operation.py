""" tests the logic/person.py"""
from . import TestConfig
from app.logic.operation import *
from app.logic.user import Users
from app.logic.person import Person, addPerson, getAge



import datetime

class TestOperationLogic(TestConfig):
	""" tests the Operation model operations """

	def test_addCountry(self):
		'''add new Country'''

		result = addCountry(name='usa', phoneCode=1, phoneLength=10, isoName='USA')

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
		'''add new operation'''

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id
		age = getAge()[0]

		# the object this operation point to
		addPerson(name='mustafa', gender='male', ageId=age.id)
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
		'''add new operation'''

		lat = 48.856613
		lng = 2.352222

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id
		age = getAge()[0]

		# the object this operation point to
		addPerson(name='mustafa', gender='male', ageId=age.id)
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

	def test_addOperation3(self):
		''' tests add Operation with full data'''

		lat = 48.856613
		lng = 2.352222

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id

		# the object this operation point to
		age = getAge()
		addPerson(name='mustafa', ageId=age[0].id, gender='male')
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='lost').first()
		status = Status_operation.query.filter_by(name='active').first()
		country = Country.query.first()

		# this long details string
		details = 'this long details string about the person'

		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.datetime.now(), lat=lat, lng=lng,
							 details=details, city='cairo', state='ciro')

		operation = Operations.query.first()


		self.assertTrue(operation)
		self.assertEqual(operation.details, details, 'not the same details')
		self.assertEqual(float(operation.lat), lat, 'not the same lat')
		self.assertEqual(float(operation.lng), lng, 'not the same lng')
		self.assertEqual(operation.object.name, person.name, 'not the same person name')

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

		result = getCountry(isoName='EG')

		self.assertEqual(result.iso_name, 'EG')
		self.assertTrue(result, 'no Country with iso_name=EG')

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
		
	def test_getOperation(self):
		""" add operation then get the operations with filters"""

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id
		age = getAge()[0]

		# the object this operation point to
		addPerson(name='mustafa', gender='male', ageId=age.id)
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='lost').first()
		status = Status_operation.query.filter_by(name='active').first()
		country = Country.query.first()

		lat = 48.856613
		lng = 2.352222

		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.date.today(), lat=lat, lng=lng)

		operation = Operations.query.first()


		self.assertTrue(operation, 'add new operation Failed')
		self.assertTrue(result, 'add new operation Failed')
		
		
		# get the operation with 'getoperation'

		# no filters
		result = getOperation()

		self.assertTrue(result, 'no operations')
		self.assertEqual(len(result), 1, 'no operations')

		# filter with object class type
		result = getOperation(object=person.__name__)
		
		self.assertTrue(result, 'no operations')
		self.assertEqual(result[0].object.name, 'mustafa')

		# filter with id
		previousOperationID = result[0].id
		result = getOperation(id=previousOperationID)
		
		self.assertTrue(result, 'no operations')
		self.assertEqual(result.id, previousOperationID)

		# filter with country id
		result = getOperation(country_id=country.id)
		
		self.assertTrue(result, 'no operations')
		self.assertEqual(result[0].object.name, 'mustafa')

		# filter with object class type and 
		result = getOperation(object=person.__name__, date=datetime.date.today())
		
		self.assertTrue(result, 'no operations')
		self.assertEqual(result[0].object.name, 'mustafa')

		# filter with object class type lat
		result = getOperation(object=person.__name__, lat=lat)
		
		self.assertTrue(result, 'no operations')
		self.assertEqual(float(result[0].lat), lat)

class TestOperationLogic3(TestConfig):

	def test_updateOperation(self):
		''' tests the update operation func'''

		# first add new operation

		# the user who make this operation
		userPublicId = Users.query.filter_by(name='admin').first().public_id
		age = getAge()[0]

		# the object this operation point to
		addPerson(name='mustafa', gender='male', ageId=age.id)
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='lost').first()
		status = Status_operation.query.filter_by(name='active').first()
		country = Country.query.first()

		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.datetime.now())

		operation = Operations.query.first()
		self.assertTrue(operation, 'add new operation Failed')

		# now change operation status
		newStatus = Status_operation.query.filter_by(name='closed').first()

		result = updateOperationStatus(operationId=operation.id, newStatus=newStatus.name)

		self.assertTrue(result, 'change not success')

		# now check the opration status
		self.assertEqual(operation.status.name, newStatus.name, 'operatuin status not changed')

		# the operatoin in the new status
		self.assertIn(operation, newStatus.operations, 'new operation not in the new status')

		# not the old status
		self.assertNotIn(operation, status.operations, 'old status not changed')

