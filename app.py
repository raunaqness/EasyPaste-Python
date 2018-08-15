from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys, os

from helpers import ipaddress, qrimage

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
		self.kwargs['progress_callback'] = self.signals.progress

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
		#Make Window Frameless
		self.setWindowFlags(Qt.FramelessWindowHint)

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
		self.vbox.setAlignment(Qt.AlignCenter)

		self.main_window.setLayout(self.vbox)
		self.main_window.setWindowFlags(Qt.FramelessWindowHint)
		self.main_window.show()
 
	def close_window(self):
		self.main_window.hide()
		# self.show()


class SystemTrayWindow():

	def __init__(self):

		self.icon = QIcon("icon.png")

		self.tray = QSystemTrayIcon()
		self.tray.setIcon(self.icon)
		self.tray.setVisible(True)

		self.menu = QMenu()

		# Button Definitions
		self.IP_button = QAction("IP")
		self.IP_button.triggered.connect(self.get_ip_address_as_qrcode)

		self.qrwindow_button = QAction("QR Code")
		self.qrwindow_button.triggered.connect(self.open_qrcode_window)

		self.about_button = QAction("About")
		self.about_button.triggered.connect(self.about)

		self.quit_button = QAction("Quit")
		self.quit_button.triggered.connect(self.exit)

		# Adding Button Actions 
		self.menu.addAction(self.qrwindow_button)
		self.menu.addAction(self.IP_button)
		self.menu.addAction(self.about_button)
		self.menu.addSeparator()
		self.menu.addAction(self.quit_button)
		
		self.tray.setContextMenu(self.menu)

	def open_qrcode_window(self):
		self.qrcode_window = QRCodeWindow()

	def get_ip_address_as_qrcode(self):
		ip = ipaddress.get_ip()
		print(ip)

	def exit(self):
		sys.exit()

	def about(self):
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


app = QApplication([])

# window = MainWindow()
tray = SystemTrayWindow()

app.exec_()
