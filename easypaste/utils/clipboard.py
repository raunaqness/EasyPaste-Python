# Housekeeping, don't mind
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

import datetime
import requests
import subprocess
import json

from utils import ipaddress

################## Main functions ##################

def data_from_android(form):
	try:
		
		# For Clipboard
		message, timestamp = parse_form(form)

		# For DB
		data = {}
		data['message'] = message
		data['timestamp'] = timestamp

		# Bhejde
		send_to_clipboard(message)
		send_to_db(data)
				
	except Exception as e:
		raiprint("Exception at data_from_android()")
		print("e = {}".format(e))

def data_from_clipboard():
	output = get_from_clipboard()

	message = ""
	timestamp = ""

	# print("CLIPBOARD-" + get_from_clipboard())
	# print(get_from_db())

	if(get_from_db() is not None):
		message, timestamp = get_from_db()

		print("message-" + str((message)))
		print("output-" + str((output)))

		if output == message:
			print("ALL GOOD")

		else:
			print("New Text in Clipboard")

			data = {}
			data['message'] = output
			data['timestamp'] = get_timestamp()

			# Send to Android
			send_to_android(data)

			# Save to db
			send_to_db(data)


def send_to_android(data):
	try:
		# TODO - Only for testing, this should be the ip for android device
		ip, h = ipaddress.get_ip()
		url = "http://" + ip + ":1234/to_android"
		r = requests.post(url = url, data = data)
	 
		# extracting response text 
		print(r.text)
	except Exception as e:
		print(e)


################## Helper Functions ##################

def send_to_db(data):
	print("Sending new data to DB")
	with open(parentdir + '/data.txt', 'w') as outfile:  
		json.dump(data, outfile)
		
def get_from_db():
	try:
		with open(parentdir + '/data.txt') as json_file:  
			data = json.load(json_file)
			message = data['message']
			timestamp = data['timestamp']
			return(message, timestamp)
	
	except Exception as e:
		print("Exception at get_from_db()")
		print("e = {}".format(e))

def get_timestamp():
	t = datetime.datetime.today().time()
	t = (str(t).split('.')[0])
	return(t)		

def get_from_clipboard():

	try:
		print("Getting from clipboard")
		cmd = 'pbpaste'
		output = subprocess.check_output(cmd, shell=True)
		output = str(output)[2:][:-1]
		return(output)
	
	except Exception as e:
		print("Exception at get_from_clipboard()")
		print("e = {}".format(e))

def send_to_clipboard(message):

	try:
		cmd = 'echo "{}" | pbcopy'.format(message)
		subprocess.call(cmd, shell=True)
		print("Sent to clipboard : {}".format(message))
		
	except Exception as e:
		print("Exception at send_to_clipboard()")
		print("e = {}".format(e))

def parse_form(form):
	try:
		d = dict(form)
		message = d['message'][0]
		timestamp = d['timestamp'][0]
		return(message, timestamp)
	
	except Exception as e:
		print("Exception at parse_form()")
		print("e = {}".format(e))

	



