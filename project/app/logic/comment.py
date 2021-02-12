from ..models import db, Comment, Users, Operations

def addComment(operationId, text, userId=None, userPublicId=None):
	''' add new comment to operation
		may use user id or public id but must choose one'''

	# first check if its valid operation and valid user
	if userId:
		user = Users.query.get(userId)
	elif userPublicId:
		user = Users.query.filter_by(public_id=userPublicId).first()
	else:
		raise ValueError('must use user id or user public id')
	
	operation = Operations.query.get(operationId)

	if not user or not operation:
		# not valid
		return False

	try:
		comment = Comment(operation_id=operationId, user_id=user.id, text=text)
		db.session.add(comment)
		db.session.commit()
	except Exception as e:
		return False

	return comment

def getComment(operationId=None, userId=None):
	''' get the comments '''

	# filter by operation id
	if operationId:
		return Comment.query.filter_by(operation_id=operationId).all()

	# filter by user
	if userId:
		return Comment.query.filter_by(user_id=userId).all()

	# all comments
	return Comment.query.all()

def deleteComment(id=None, object=None, operationId=None):
	''' deltet the comment - if no filter passed Error will be raised'''

	# list of comments
	if operationId:
		comments = Comment.query.filter_by(operation_id=operationId).delete()
		db.session.commit()
		return True

	if id:
		comment = Comment.query.get(id)
	
	elif object:
		comment = object


	# raise error
	if not comment:
		raise ValueError('must pass filters to delete')

	# delete the car
	db.session.delete(comment)

	db.session.commit()	

	return True
