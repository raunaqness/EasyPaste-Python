from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys, os

import socket  
import time
import subprocess

from utils import ipaddress, qrimage

class testclass():

	def add(self, a, b):
		return(a+b)


def add(a, b):
	return(a+b)

class WorkerSignals(QObject):

	finished = pyqtSignal()
	error = pyqtSignal(tuple)
	result = pyqtSignal(object)
	progress = pyqtSignal(int)

class Worker(QRunnable):

	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()

		# Store constructor arguments (re-used for processing)
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()

		# Add the callback to our kwargs
		# self.kwargs['progress_callback'] = self.signals.progress

	@pyqtSlot()
	def run(self):

		try:
			result = self.fn(*self.args, **self.kwargs)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)  # Return the result of the processing
		finally:
			self.signals.finished.emit()  # Done

class QRCodeWindow(QWidget):
 
	def __init__(self):
		super().__init__()
		self.initUI()
 
	def initUI(self):
		
		# Put Window in the Centre of the screen
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)

		self.move(frameGm.topLeft())

		self.main_window = QWidget()
		self.vbox = QVBoxLayout()

		# Get QR Code Image
		ip_address = ipaddress.get_ip()
		img = qrimage.get_qrimage(ip_address)

		# Create QRCode Image Holder
		self.qrcode_image_holder = QLabel()
		self.pixmap = QPixmap.fromImage(img)
		self.qrcode_image_holder.setPixmap(self.pixmap)
		self.qrcode_image_holder.resize(self.pixmap.width(), self.pixmap.height())

		# Description 
		self.description = QLabel()
		self.description.setText("Scan the QR Code with EasyPaste Android App to Connect")
		self.description.setAlignment(Qt.AlignCenter)

		# Close Button
		self.close_button = QPushButton("Close")
		self.close_button.clicked.connect(self.close_window)

		self.vbox.addWidget(self.qrcode_image_holder)
		self.vbox.addWidget(self.description)
		self.vbox.addWidget(self.close_button)

		self.qrcode_image_holder.setAlignment(Qt.AlignCenter)
		self.description.setAlignment(Qt.AlignCenter)
		self.vbox.setAlignment(Qt.AlignCenter)

		self.palette = QPalette()
		self.palette.setColor(QPalette.Background, Qt.white)
		self.main_window.setPalette(self.palette)

		self.main_window.setLayout(self.vbox)
		# self.main_window.setWindowFlags(Qt.FramelessWindowHint)
		self.main_window.show()
 
	def close_window(self):
		self.main_window.hide()
		# self.show()

	def divide(self, a, b):
		if(b is not 0):
			return(a/b)

class SystemTrayWindow():


	def __init__(self):

		self.icon = QIcon("images/icon.png")

		self.tray = QSystemTrayIcon()
		self.tray.setIcon(self.icon)
		self.tray.setVisible(True)

		self.menu = QMenu()

		# socket variable definitions
		self.threadpool = QThreadPool()

		self.socket_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.ip_address = ipaddress.get_ip()
		self.server_address_send = (self.ip_address, 1234)

		self.server_address_receive = (self.ip_address, 1234)
		self.socket_receive.bind(self.server_address_receive)
		self.socket_receive.listen(1)

		self.last_message = ""

		# Button Definitions
		self.qrwindow_button = QAction("Connect")
		self.qrwindow_button.triggered.connect(self.open_qrcode_window)

		self.about_button = QAction("About")
		self.about_button.triggered.connect(self.about)

		self.quit_button = QAction("Quit")
		self.quit_button.triggered.connect(self.exit)

		# Adding Button Actions 
		self.menu.addAction(self.qrwindow_button)
		# self.menu.addAction(self.IP_button)
		self.menu.addSeparator()
		self.menu.addAction(self.about_button)
		self.menu.addAction(self.quit_button)
		
		self.tray.setContextMenu(self.menu)

		self.initialize_socket_worker()

	def initialize_socket_worker(self):
		socket_worker = Worker(self.main_socket_function_to_thread)
		self.threadpool.start(socket_worker)
		

	# Socket Functions

	def main_socket_function_to_thread(self):

		while True:
			latest_message = self.get_from_socket()
			print("latest_message : {}".format(latest_message))

			if latest_message is not self.last_message:
				self.last_message = latest_message
				self.send_to_clipboard(latest_message)

			time.sleep(1)

	def get_from_socket(self):
		print("Getting from Socket")
		try:
			connection, client_address = self.socket_receive.accept()
			data = connection.recv(64)
			print(data)
			return(str(data))
		except:
			print("No data Received")

	def send_to_clipboard(self, message):
		cmd = 'echo "{}" | pbcopy'.format(message)
		subprocess.call(cmd, shell=True)
		print("Sent to clipboard : {}".format(message))



	# Helper Functions

	def open_qrcode_window(self):
		self.qrcode_window = QRCodeWindow()

	def exit(self):
		sys.exit()

	def about(self):
		# TODO
		pass


class MainWindow(QMainWindow):


	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.counter = 0

		layout = QVBoxLayout()

		self.l = QLabel("Start")
		b = QPushButton("DANGER!")
		b.pressed.connect(self.oh_no)

		layout.addWidget(self.l)
		layout.addWidget(b)

		w = QWidget()
		w.setLayout(layout)

		self.setCentralWidget(w)

		self.show()

		self.threadpool = QThreadPool()
		print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()

	def progress_fn(self, n):
		print("%d%% done" % n)

	def execute_this_fn(self, progress_callback):
		for n in range(0, 5):
			time.sleep(1)
			progress_callback.emit(n*100/4)

		return "Done."

	def print_output(self, s):
		print(s)

	def thread_complete(self):
		print("THREAD COMPLETE!")

	def oh_no(self):
		# Pass the function to execute
		worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
		worker.signals.result.connect(self.print_output)
		worker.signals.finished.connect(self.thread_complete)
		worker.signals.progress.connect(self.progress_fn)

		# Execute
		self.threadpool.start(worker)


	def recurring_timer(self):
		self.counter +=1
		self.l.setText("Counter: %d" % self.counter)

if __name__ == "__main__":
	app = QApplication([])

	# window = MainWindow()
	tray = SystemTrayWindow()

	app.exec_()
