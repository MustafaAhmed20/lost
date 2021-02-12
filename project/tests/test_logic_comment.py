""" tests the logic/comment.py"""
from . import TestConfig
from app.logic.comment import *

# the operation-related logic
from app.logic.user import Users
from app.logic.person import Person, addPerson, getAge
from app.logic.operation import *


class TestCommentLogic(TestConfig):
	""" tests the commenting system """

	def test_addComment(self):
		''' add operation then add comments to it'''

		# first add the operation
		#

		userPublicId = Users.query.filter_by(name='admin').first().public_id
		age = getAge()[0]

		# the object this operation point to
		addPerson(name='mustafa', gender='male', ageId=age.id)
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='lost').first()
		status = Status_operation.query.filter_by(name='active').first()
		country = Country.query.first()

		import datetime
		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.datetime.now())

		operation = Operations.query.first()
		self.assertTrue(operation, 'add new operation Failed')

		# now add comment to the operation
		#

		comment =  addComment(operationId=operation.id, userPublicId = userPublicId, text='this test comment')
		self.assertTrue(comment, 'add new comment Failed')

		# check the comment in the database

		newComment = Comment.query.first()
		self.assertTrue(newComment, 'add new comment in the database Failed')

		comments = operation.comments.all()
		self.assertEqual(len(comments), 1, 'not same number of comments')

		# try get the comments
		allComments = getComment()
		self.assertTrue(allComments, 'no comments returned')
		self.assertEqual(len(allComments), 1, 'not same number of comments')

		# filter with operation
		operationComments = getComment(operationId=operation.id)
		self.assertTrue(operationComments, 'no comments returned')
		self.assertEqual(len(operationComments), 1, 'not same number of comments')

		# now delete the comment
		result = deleteComment(operationId=operation.id)

		self.assertTrue(result)

		# check the comments in the database
		comments = Comment.query.all()
		self.assertFalse(comments, 'the comments didn\'t deleted')
	
	def test_deleteComment(self):
		''' try delete the comments with different filters'''

		# first add the operation
		#

		userPublicId = Users.query.filter_by(name='admin').first().public_id
		age = getAge()[0]

		# the object this operation point to
		addPerson(name='mustafa', gender='male', ageId=age.id)
		person = Person.query.first()
		
		type = Type_operation.query.filter_by(name='lost').first()
		status = Status_operation.query.filter_by(name='active').first()
		country = Country.query.first()

		import datetime
		result = addOperation(type=type, status=status, country=country, object=person,\
							 userPublicId= userPublicId, date=datetime.datetime.now())

		operation = Operations.query.first()
		self.assertTrue(operation, 'add new operation Failed')

		# now add comment to the operation
		#

		comment =  addComment(operationId=operation.id, userPublicId = userPublicId, text='this test comment')
		self.assertTrue(comment, 'add new comment Failed')

		
		# delete with operation id
		result = deleteComment(operationId=operation.id)
		self.assertTrue(result)

		# check the comments in the database
		comments = Comment.query.all()
		self.assertFalse(comments, 'the comments didn\'t deleted')

		# add comment again
		comment =  addComment(operationId=operation.id, userPublicId = userPublicId, text='this test comment')
		self.assertTrue(comment, 'add new comment Failed')
		
		
		# delete with comment id
		result = deleteComment(id=comment.id)
		self.assertTrue(result)

		# check the comments in the database
		comments = Comment.query.all()
		self.assertFalse(comments, 'the comments didn\'t deleted')

		# add comment again
		comment =  addComment(operationId=operation.id, userPublicId = userPublicId, text='this test comment')
		self.assertTrue(comment, 'add new comment Failed')
		
		
		# delete with comment object
		result = deleteComment(object=comment)
		self.assertTrue(result)

		# check the comments in the database
		comments = Comment.query.all()
		self.assertFalse(comments, 'the comments didn\'t deleted')
