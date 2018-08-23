from flask import Flask, render_template


app = Flask(__name__)
app.debug = False
app.use_reloader = False


@app.route('/')
def index():
	print("GG")
	return("GG")