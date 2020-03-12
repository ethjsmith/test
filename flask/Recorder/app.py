from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#url = "test"
app.secret_key = "secret :)"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all()
class Record(db.Model):
	key = db.Column(db.Integer(), primary_key=True)
	data = db.Column(db.String())
	def __init__(self,data):
		self.data = data
	def __repr__(self):
		ret = str(self.key) + ": [" + self.data + "]"
		return ret

@app.route("/")
def testfunc():
	z = Record.query.all()
	ret = "attempted passwords: <br>"
	for x in z:
		ret += str(x) + "<br>"
	return ret

@app.route("/insert/<path:thing>")
def test2(thing):
	a = Record(thing)
	db.session.add(a)
	db.session.commit()
	return redirect('/')

@app.route("/remove/<path:targ>")
def rem(targ):
	dele = Record.query.filter_by(key=targ).delete()
	db.session.commit()
	return redirect("/")

if (__name__ == "__main__"):
	app.run()
