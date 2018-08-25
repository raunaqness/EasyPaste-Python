# Housekeeping, don't mind
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

import subprocess
import json

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
		send_to_json(data)
				
	except Exception as e:
		raiprint("Exception at data_from_android()")
		print("e = {}".format(e))


################## Helper Functions ##################

def send_to_json(data):
	import json

	data = {}  
	data['message'] = "message"
	data['timestamp'] = "timestamp"

	with open(parentdir + '/data.txt', 'w') as outfile:  
	    json.dump(data, outfile)

def get_from_clipboard():

	try:
		print("Getting from clipboard")
		cmd = 'pbpaste'
		output = subprocess.check_output(cmd, shell=True)
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

	



