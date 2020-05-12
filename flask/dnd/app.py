from flask import Flask,render_template, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#url = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = 'zzz'
db = SQLAlchemy(app)
db.create_all()

class Character(db.Model):
	__tablename__ = "Character"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	role = db.Column(db.String())
	spells = db.relationship('Spell', backref ='Spell', lazy='dynamic', primaryjoin="Character.id == Spell.parent_id")
	# how are spells and character linked ? I'm bad atthis
	def __init__(self,name,role):
		self.name=  name
		self. role = role


class Spell(db.Model):
	__tablename__ = 'Spell'
	id = db.Column(db.Integer, primary_key=True)
	parent_id = db.Column(db.Integer, db.ForeignKey("Character.id"))
	spellname = db.Column(db.String())
	cooldown = db.Column(db.Integer())
	current = db.Column(db.Integer())
	def __init__(self,sname,coold):
		self.spellname = sname
		self.cooldown = coold
		self.current = 0
	# This should happen at the start of a turn :^) because that's how I think it should be
	def dec(self):
		if self.current > 0:
			self.current -= 1
	def cast(self):
		self.current = self.current + self.cooldown
		print(self.current)

@app.route("/")
def testfunc():
	spells = Spell.query.all()
	for s in spells:
		print(s.current)
	return render_template("spellpage.html", spells=spells)

@app.route("/cast/<path:spell>")
def castme(spell):
	casted = Spell.query.filter_by(id=spell).first()
	if casted.current == 0:
		casted.cast()
	db.session.commit()
	return redirect("/")

@app.route("/takeTurn")
def do():
	spells = Spell.query.all()
	for spell in spells:
		spell.dec()
	db.session.commit()
	return redirect("/")
@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
