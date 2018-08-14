import socket  
import time
import subprocess 

socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '0.0.0.0'
server_address_send = (ip_address, 1234)

# For Receiving
server_address_receive = (ip_address, 4567)
socket_receive.bind(server_address_receive)
socket_receive.listen(1)


last_message = ""

def main():
	global last_message

	while True:
		latest_message = get_from_socket()
		print("latest_message : {}".format(latest_message))

		if latest_message is not last_message:
			last_message = latest_message
			send_to_clipboard(latest_message)

		time.sleep(3)


def send_to_clipboard(message):
	cmd = 'echo "{}" | pbcopy'.format(message)
	subprocess.call(cmd, shell=True)
	print("Sent to clipboard : {}".format(message))

def get_from_clipboard():
	cmd = 'pbpaste'
	output = subprocess.check_output(cmd, shell=True)
	return(output)


def get_from_socket():
	print("Getting from Socket")

	try:
		print("1")
		connection, client_address = socket_receive.accept()
		print("2")
		data = connection.recv(64)
		print("3")
		print(data)
		return(str(data))

	except:
		print("No data Received")


def send_to_socket(message):
	data = str(message)
	sock.sendall(data)

if __name__ == "__main__":
	main()
