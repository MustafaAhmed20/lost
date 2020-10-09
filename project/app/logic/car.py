from ..models import db, Car
from .person import deletePhoto

# car model
def addCar(type, plateNumberLetters, plateNumberNumbers, brand, model):
	''' add new car - return Car object if success else False'''
	plateNumber = '-'.join([plateNumberLetters, plateNumberNumbers])
	try:
		car = Car(type=type, plate_number=plateNumber, model=model, brand=brand)
		db.session.add(car)
		db.session.commit()
	except Exception as e:
		return False

	return car

def getCar(id=None, type=None, plateNumberLetters=None, plateNumberNumbers=None):
	""" return the Car object or None if not exist
		return a list of all Cars if no filters passed.
		return one object if filtered by 'id' or  plateNumber"""

	if id:
		return Car.query.get(id)

	if plateNumberLetters and plateNumberNumbers:
		plateNumber = '-'.join([plateNumberLetters, plateNumberNumbers])

		return Car.query.filter_by(plate_number=plateNumber).first()

	if type:
		return Car.query.filter_by(type=type).all()

	if not any([id, type]):
		return Car.query.all()


	return None

def deleteCar(id=None, object=None):
	""" delete the photos then delete the car
		perm : object = the car object"""

	if id:
		car = Car.query.get(id)
	elif object:
		car = object

	if not car:
		return False

	# delete the photos
	deletePhoto(car)

	# delete the car
	db.session.delete(car)

	db.session.commit()	

	return True