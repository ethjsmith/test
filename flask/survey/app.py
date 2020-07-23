from flask import Flask,render_template, redirect,g, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#url = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = 'zzz'
db = SQLAlchemy(app)
db.create_all()
app = Flask(__name__)
#url = "test"

class Entry(db.Model):
	__tablename__ = "Entry"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String())
	color = db.Column(db.String())
	def __init__(self,name,color):
		self.name = name
		self.color = color

# character has spell slots

# characters has attuned spells






@app.route("/")
def testfunc():
	return redirect("/entry")

@app.route("/entry", methods = ["GET","POST"])
def entry():
	return render_template("entry.html")

@app.route("/view", methods = ["GET","POST"])
def view():
	return render_template("result.html")

if (__name__ == "__main__"):
	app.run()
