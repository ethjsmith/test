from flask import Flask
import datetime
#import urllib.parse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#url = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = 'zzz'
db = SQLAlchemy(app)
db.create_all()

class Thing(db.Model):
	__tablename__ = "Thing"
	id= db.Column(db.Integer, primary_key= True)
	data = db.Column(db.String())
	date = db.Column(db.String())
	time = db.Column(db.String())
	def __init__(self,data):
		self.data = data
		self.date = datetime.date.today().strftime('%b %d, %Y')
		self.time = datetime.datetime.now().strftime('%H:%M')
	def __str__(self):
		return date
@app.route("/")
def testfunc():
	return "this is a test boys"

@app.route("/<path:url>")
def test2(url):
	a = Thing(url)
	db.session.add(a)
	db.session.commit()
	return "your url is " + url
@app.route('/time')
def time():
	return datetime.datetime.now().strftime('%H:%M')
# lets you see the saved URLS
@app.route('/seeurls')
def see():
	tmp = str(datetime.date.today().strftime('%b %d, %Y'))
	returns = Thing.query.filter_by(date=tmp)
	retme = ""
	for x in returns:
		retme += x.data + '__ at:' + x.time + "<br>"
	return retme

if (__name__ == "__main__"):
	app.run()
