from flask import Flask,render_template, redirect,g, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#url = "test"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = 'zzz'
db = SQLAlchemy(app)
db.create_all()
#session['char'] = None
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
	def __init__(self,sname,coold,pid):
		self.spellname = sname
		self.cooldown = int(coold) + 1
		self.current = 0
		self.parent_id = pid
	# This should happen at the start of a turn :^) because that's how I think it should be
	def dec(self):
		if self.current > 0:
			self.current -= 1
	def cast(self):
		self.current = self.current + self.cooldown


# check to make sure you have a character selected when you try to interact with the spells
def char_selected(f):
#	@wraps(f)
	def wrap(*args, **kwargs):
		if g.character != None:
			return f(*args, **kwargs)
		else:
			return redirect("/char")
	wrap.__name__=f.__name__
	return wrap

@app.before_request
def before():
    """Sets up variables before each function runs"""
    g.character = None
    g.charname = "None Selected"
    if 'character' in session:
        g.character = session['character']
        g.charname = Character.query.filter_by(id=g.character).first()
        #g.charname = x.name

# gives templates access to all stuff :)
@app.context_processor
def giveFunctions():
	def getCharacters():
		charz = Character.query.all()
		return charz
	def getSpells(id=None):
		if id is not None:
			Spel = Spell.query.filter_by(parent_id=id).all()
		else:
			Spel = Spell.query.all()
		return Spel
	return dict(getCharacters=getCharacters,getSpells=getSpells)

@app.route("/a")
def tfun():
	chars = Character.query.all()
	for char in chars:
		print(char.name + ": " + str(char.id))
		spel = Spell.query.filter_by(parent_id=char.id).all()
		for spe in spel:
			print(spe.spellname)
		print("--------------")
	return "Go check the logs here :) "

@app.route("/", methods = ["GET","POST"])
@char_selected
def testfunc():
	if request.method == "POST" and 'spellname' in request.form and 'level' in request.form:
		a = Spell(request.form["spellname"],request.form["level"],g.character)
		db.session.add(a)
		db.session.commit()
	spells = Spell.query.filter_by(parent_id = g.character).all()
	return render_template("spellpage.html", spells=spells)

@app.route("/char", methods = ["GET","POST"])
def char_select():
	if request.method == "POST":
		if 'uname' in request.form and 'cname' in request.form:
			a = Character(request.form['uname'],request.form['cname'])
			db.session.add(a)
			db.session.commit()
			zz = Character.query.filter_by(name=request.form['uname']).first()
			session['character'] = zz.id
		else:
			session["character"] = request.form['character']
		return redirect("/")
	return render_template("chars.html", chars=Character.query.all())


@app.route("/cast/<path:spell>")
@char_selected
def castme(spell):
	casted = Spell.query.filter_by(id=spell).first()
	if casted.current == 0:
		casted.cast()
	db.session.commit()
	return redirect("/")

@app.route("/takeTurn")
@char_selected
def do():
	spells = Spell.query.filter_by(parent_id = g.character).all()
	for spell in spells:
		spell.dec()
	db.session.commit()
	return redirect("/")


if (__name__ == "__main__"):
	app.run()
