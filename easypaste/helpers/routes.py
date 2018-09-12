# Housekeeping, don't mind
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from flask import Flask, render_template, request
from utils import clipboard 

app = Flask(__name__)

app.use_reload = False
app.debug = False

@app.route('/')
def index():
	print("GG")
	return("GG")

@app.route("/data_from_android", methods=['GET', 'POST'])
def data_from_android():
	if request.method == 'POST':
		form = request.form
		print(str(form))
		clipboard.data_from_android(form)
		return("POST Succesful")

	if request.method == 'GET':
		return("GET Succesful")

@app.route("/ack_from_android", methods=['GET', 'POST'])
def ack_from_android():
	if request.method == 'POST':
		form = request.form
		print(str(form))
		clipboard.ack_from_android(form)
		return("POST Succesful")


# For Testing
@app.route("/to_android", methods=['POST'])
def to_android():
	if request.method == 'POST':
		form = request.form
		# print(str(form))
		return("Android POST Succesful")


