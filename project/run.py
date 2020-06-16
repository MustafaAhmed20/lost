from app import fullApp

from dotenv import load_dotenv


if __name__ == "__main__":

	# load the variables from the env file!
	load_dotenv()

	# Run the server.
	fullApp.run(host='0.0.0.0', port=8080)
