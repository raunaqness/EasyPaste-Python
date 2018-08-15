import subprocess
import re

def get_ip():
	cmd = 'ifconfig |grep inet'
	output = subprocess.check_output(cmd, shell=True)

	words = str(output).split(' ')
	ips = []
	final_ip = ""

	for word in words:
		match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", word)
		if match is not None:
			ips.append(match.group(0))
				
	for ip in ips:
		if('127.0.0.1' not in ip):
			final_ip = ip
			break

	return(final_ip)