from . import api

@api.route('/login', methods=['POST'])
def login():
	pass

@api.route('/logout', methods=['POST'])
def logout():
	pass

@api.route('/adduser', methods=['POST'])
def addUser():
	pass

@api.route('/deleteuser', methods=['DELETE'])
def deleteUser():
	pass

@api.route('/changeuserpermission', methods=['DELETE'])
def changeUserPermission():
	pass


