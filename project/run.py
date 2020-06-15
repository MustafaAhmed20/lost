from app import fullApp


if __name__ == "__main__":

	# Configurations
	fullApp.config.from_object('config')
	
	# Run a test server.
	fullApp.run(host='0.0.0.0', port=8080, debug=True)