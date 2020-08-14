#!/home/dh_67mu4w/losthope.me/env/bin/python3
import sys
from flup.server.fcgi import WSGIServer
from run import check_database, fullApp

if __name__ == '__main__':
	check_database()

	WSGIServer(fullApp).run()