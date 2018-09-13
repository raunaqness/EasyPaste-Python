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

def payload_from_android(payload):
	print(parentdir)
	try:
		# For Clipboard
		payload = dict(payload)

		# Check the type of Data received (ACK, MSG, or IMG)
		payload_type = payload['payload_type'][0]
		print("Payload : ", payload_type)

		if('Acknowledgement' in payload_type):
			# Connection established. Acknowledgement received
			android_ip = payload['data'][0]
			print("android_ip-", android_ip)

			data = get_from_db()
			data['android_ip'] = android_ip

			print("FINAL-", str(data))
			send_to_db(data)


		elif('ClipText' in payload_type):
			# Clipboard Text. Send to Clipboard

			pass

		elif('Image' in payload_type):
			# Image sent. TODO

			pass

		else:
			print("Unknown Payload Type")

		

		# Bhejde
		# send_to_clipboard(data['message'])
		# send_to_db(data)
				
	except Exception as e:
		print("Exception at data_from_android()")
		print("e = {}".format(e))

def ack_from_android(form):
	try:
		form = dict(form)
		data = get_from_db()

		# For DB
		data['android_ip'] = form['message'][0]
		data['timestamp'] = form['timestamp'][0]

		# Bhejde
		send_to_db(data)
				
	except Exception as e:
		print("Exception at ack_from_android()")
		print("e = {}".format(e))

def data_from_clipboard():
	try:
		output = get_from_clipboard()

		message = ""
		timestamp = ""

		# print("CLIPBOARD-" + get_from_clipboard())
		# print(get_from_db())

		if(get_from_db() is not None):
			data = get_from_db()
			message, timestamp = data['cliptext'], data['timestamp']

			print("message-" + str((message)))
			print("output-" + str((output)))

			if output == message:
				print("ALL GOOD")

			else:
				print("New Text in Clipboard")

				data['cliptext'] = output
				data['timestamp'] = get_timestamp()

				# Send to Android

				send_to_android("MSG", output)

				# Save to db
				send_to_db(data)

	except Exception as e:
		print("Exception at data_from_clipboard()")
		print("e = {}".format(e))


def send_to_android(payload_type, payload_data):

	'''
	Payload should be one of the following types = 'ACK' or 'MSG'
	'''

	try:
		print("Sending to Android")
		data = get_from_db()
		android_ip = data['android_ip']
		
		url = "http://" + android_ip + ":8080"

		payload = {}
		payload['payload_type'] = payload_type
		payload['payload_data'] = payload_data
		json.dumps(payload)

		print("Payload_to_Android", str())

		headers = { 'Content-Type': 'application/json' }

		r = requests.post(url = url, data = payload, headers = headers)
	 
		# extracting response text 
		print(r.text)
	except Exception as e:
		print("Exception at send_to_android()")
		print("e = {}".format(e))


################## Helper Functions ##################

def send_to_db(data):
	print("Sending new data to DB")
	with open(parentdir + '/data.txt', 'w') as outfile:  
		json.dump(data, outfile)
		
def get_from_db():
	if(not os.path.exists(parentdir + '/data.txt')):
		data = {}
		data['android_ip'] = ""
		data['cliptext'] = ""
		data['timestamp'] = ""
		send_to_db(data)

	try:
		with open(parentdir + '/data.txt') as json_file:  
			data = json.load(json_file)
			# message = data['message']
			# timestamp = data['timestamp']
			return(data)
	
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



	



