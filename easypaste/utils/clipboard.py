import subprocess

def get_from_clipboard():
	cmd = 'pbpaste'
	output = subprocess.check_output(cmd, shell=True)
	return(output)

def send_to_clipboard(form):

	message, timestamp = parse_form(form)

	cmd = 'echo "{}" | pbcopy'.format(message)
	subprocess.call(cmd, shell=True)
	print("Sent to clipboard : {}".format(message))

def parse_form(form):
	d = dict(form)

	message = d['message'][0]
	timestamp = d['timestamp'][0]

	return(message, timestamp)
