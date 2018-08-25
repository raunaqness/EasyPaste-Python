from flask import Flask, render_template, request

app = Flask(__name__)

app.use_reload = False
app.debug = False

@app.route('/')
def index():
	print("GG")
	return("GG")

@app.route("/from_android", methods=['GET', 'POST'])
def from_android():
	if request.method == 'POST':
		form = request.form
		print(str(form))
		return("POST Succesful")

	if request.method == 'GET':
		return("GET Succesful")