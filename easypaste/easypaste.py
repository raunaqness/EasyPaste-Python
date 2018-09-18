from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import traceback
import sys
import time

from utils import ipaddress, qrimage, clipboard

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.environ.get("_MEIPASS2",os.path.abspath("."))

	return os.path.join(base_path, relative_path)

class testclass():

	def add(self, a, b):
		return(a+b)

################## Worker Classes ##################

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

################## PyQt UI Functions ##################

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
		ip_address, hostname = ipaddress.get_ip()
		img = qrimage.get_qrimage(ip_address + " | " + hostname)

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

class SystemTrayWindow:

	def __init__(self):

		self.icon = QIcon(resource_path("images/icon.png"))

		self.tray = QSystemTrayIcon()
		self.tray.setIcon(self.icon)
		self.tray.setVisible(True)

		self.menu = QMenu()

		self.threadpool = QThreadPool()

		self.last_message = ""

		# Button Definitions
		self.qrwindow_button = QAction("Connect")
		self.qrwindow_button.triggered.connect(self.open_qrcode_window)

		self.take_photo_button = QAction("Take Photo")
		self.take_photo_button.triggered.connect(self.take_photo)

		self.about_button = QAction("About")
		self.about_button.triggered.connect(self.about)

		self.quit_button = QAction("Quit")
		self.quit_button.triggered.connect(self.exit)

		# Adding Button Actions 
		self.menu.addAction(self.qrwindow_button)

		self.menu.addSeparator()
		self.menu.addAction(self.take_photo_button)

		self.menu.addSeparator()
		self.menu.addAction(self.about_button)
		self.menu.addAction(self.quit_button)
		
		self.tray.setContextMenu(self.menu)

		# Start Threads

		self.start_flask_thread()
		self.start_background_thread()

	# Worker Functions and Definitions

	def start_flask_thread(self):
		flask_worker = Worker(self.flask_thread)
		self.threadpool.start(flask_worker)

	def flask_thread(self):
		from helpers.routes import app 
		self.host, _ = ipaddress.get_ip()
		self.port = 1234
		app.run(host=self.host, port=self.port)

	# Background Clipboard Checking Functions and Definitions

	def start_background_thread(self):
		background_worker = Worker(self.background_thread)
		self.threadpool.start(background_worker)

	def background_thread(self):
		time.sleep(5)
		while True:
			clipboard.data_from_clipboard()
			time.sleep(3)

	# Helper Functions

	def take_photo(self):
		clipboard.send_to_android("Image", "Take Photo")

	def open_qrcode_window(self):
		self.qrcode_window = QRCodeWindow()

	def exit(self):
		sys.exit()

	def about(self):
		# TODO
		pass

if __name__ == "__main__":
	app = QApplication([])

	tray = SystemTrayWindow()

	app.exec_()
