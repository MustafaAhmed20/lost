from app import fullApp

def check_database():
	"""check if the database found. if not , create the database and then create the tables.
	NOTE: this part work with mysql database, 
	if you use any other database you may consider this part and make the necessary changes """
	from app.models import db
	from flask_sqlalchemy import sqlalchemy
	import os
	
	e = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
	
	existing_databases = e.execute("SHOW DATABASES;")
	# Results are a list of single item tuples, so unpack each tuple
	existing_databases = [d[0] for d in existing_databases]

	# Create database if not exists
	if os.getenv('DATABASE_NAME_DEVELOPMENT') not in existing_databases:

		e.execute(f"CREATE DATABASE {os.getenv('DATABASE_NAME_DEVELOPMENT')}")

		# now create the tables 
		db.create_all(app=fullApp)

if __name__ == "__main__":
	
	# check the database before running!
	check_database()
	
	# Run the server.
	#fullApp.run(host='0.0.0.0', port=8080)
	fullApp.run()
