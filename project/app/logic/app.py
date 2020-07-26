''' this model contain the logic for app-related functionality'''
import re

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

