from app import fullApp

from dotenv import load_dotenv


if __name__ == "__main__":

	# load the variables from the env file !
	load_dotenv()

	# Configurations
	fullApp.config.from_object('config')
	
	# Run a test server.
	fullApp.run(host='0.0.0.0', port=8080)
