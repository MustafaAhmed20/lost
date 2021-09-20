''' this model contain the logic for app-related functionality'''
import re

from ..models import db, Feedback

def validatePhoneNumber(value, countryCode, maxPhoneLength):
	''' validate and extract the phone number
		value 			: the phone interd by the user
		countryCode 	: the country phone-code the user rigster in
		maxPhoneLength 	: the max length of the phone number without the beginning zero

		return the actual phone number if matched
		return False if not match'''
	
	if not value:
		# emptiness not checked here
		raise ValueError('value must not be empty')

	# remove any spaces
	value = value.replace(' ', '')


	pattren = fr'^(?:((\+|00)?(?P<code>{countryCode}))|0)?(?P<phone>\d{ {maxPhoneLength} })$'

	match = re.search (pattren, value)

	if not match:
		return False

	# return only the actual number
	return match.group('phone')

def validatePassword(value, minLength):
	''' validate the password with 
		return True if passed the validtion else False'''

	if not value:
		# emptiness not checked here
		raise ValueError('value must not be empty')

	
	##
	## trial period - TODO: change back when lunch

	# if len(value) < minLength:
	# 	return False

	# must contain at least one number
	pattren1 = r'\d'

	# must contain at least one letter
	pattren2 = r'[a-zA-Z]'

	# if not re.search (pattren1, value) or not re.search (pattren2, value):
	if not re.search (pattren2, value):
		return False

	return True

# Feedback modele
def addFeedback(text, userPublicId=None):

	feedback = Feedback(feedback=text, user_public_id=userPublicId)
	db.session.add(feedback)
	db.session.commit()

	return True

def getFeedback(userPublicId=None):

	if not userPublicId:
		# return all
		return Feedback.query.all()

	# feedback from one user
	return Feedback.query.filter_by(user_public_id=userPublicId).all()

def deleteFeedback(userPublicId=None, id=None):

	# if no data submited return false
	if not userPublicId and not id:
		return False

	if id:
		feedback = Feedback.query.filter(Feedback.id == id).delete()
		db.session.commit()
		return True
	if userPublicId:
		feedback = Feedback.query.filter_by(user_public_id=userPublicId).delete()
		db.session.commit()
		return True

