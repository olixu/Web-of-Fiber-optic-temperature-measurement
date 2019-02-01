import socket 
import sys 
import os
import struct
import time
HOST = "173.82.168.157"
PORT =5000 

filenames = os.listdir('.')
#print(filenames)

def scan():
	global filenames
	while(True):
		new_filenames = os.listdir('.')
		for filename in new_filenames:
			if filename not in filenames:
				upload(filename)
				print("Now is uploading file: %s" % filename)
		filenames = new_filenames
		time.sleep(0.2)


def upload(filename):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	print("Connected with server")
	with open(filename, "rb") as f:
		print("Sending file...")
		data = f.read()
		s.sendall(data)

		s.close()
		print("Disconnected")
		#sys.exit(0)

scan()

