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
	items = db.relationship("Item", backref = "Item", lazy = 'dynamic', primaryjoin="Character.id == Item.owner")
	# how are spells and character linked ? I'm bad atthis
	def __init__(self,name,role):
		self.name =  name
		self.role = role


class Spell(db.Model):
	__tablename__ = 'Spell'
	id = db.Column(db.Integer, primary_key=True)
	parent_id = db.Column(db.Integer, db.ForeignKey("Character.id"))
	spellname = db.Column(db.String())
	cooldown = db.Column(db.Integer())
	current = db.Column(db.Integer())
	def __init__(self,sname,coold,pid):
		if int(coold) < 0:
			self.cooldown == 0
		else:
			self.cooldown = int(coold)
		self.spellname = sname
		self.current = 0
		self.parent_id = pid
		# This now happens at the end of the turn, because that's better :^)
	def dec(self):
		if self.current > 0:
			self.current -= 1
	def cast(self):
		self.current = self.current + self.cooldown
# Item class, for items or daily powers, whatever really :^)
class Item(db.Model):
	__tablename__ = "Item"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	owner = db.Column(db.Integer, db.ForeignKey("Character.id"))
	# renewable = 0 item dissapears when uses gone 1 = recharges with long rest 2 = recharges with special condition
	renewable = db.Column(db.Integer())
	uses = db.Column(db.Integer())
	current = db.Column(db.Integer())
	def __init__(self,iname,pid,renew,use):
		self.name = iname
		self.owner = pid
		self.renewable = renew
		self.uses = use
		self.current = use
	def canuse(self):
		if self.current > 0:
			return True
		return False
	# dont forget a db.commit() after a use or a rest :^)
	def use(self):
		self.current -= 1
	def rest(self):
		if self.renewable == 3:
			self.current = self.uses
	def charge(self,ch):
		self.current += int(ch)
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

@app.route("/", methods = ["GET","POST"])
@char_selected
def testfunc():
	if request.method == "POST" and 'spellname' in request.form and request.form["spellname"] != "" and request.form['level'] != "":
		a = Spell(request.form["spellname"],request.form["level"],g.character)
		db.session.add(a)
		db.session.commit()
	elif request.method == "POST" and 'itemname' in request.form and request.form['itemname'] != "" and request.form['uses'] != "" and request.form['type'] != "":
		print("making item")
		a = Item(request.form["itemname"],g.character,request.form["type"],request.form["uses"])
		db.session.add(a)
		db.session.commit()
	spells = Spell.query.filter_by(parent_id = g.character).order_by(Spell.cooldown.asc()).all()
	items = Item.query.filter_by(owner = g.character).order_by(Item.renewable.asc()).all()
	return render_template("spellpage.html", spells=spells, items=items)

@app.route("/char", methods = ["GET","POST"])
def char_select():
	if request.method == "POST":
		if 'uname' in request.form and 'cname' in request.form and request.form['uname'] != "" and request.form["cname"] != "":
			a = Character(request.form['uname'],request.form['cname'])
			db.session.add(a)
			db.session.commit()
			zz = Character.query.filter_by(name=request.form['uname']).first()
			session['character'] = zz.id
		else:
			session["character"] = request.form['character']
		return redirect("/")
	return render_template("chars.html", chars=Character.query.all())
# route for using items
@app.route("/use/<path:item>")
@char_selected
def useme(item):
	used = Item.query.filter_by(id=item).first()
	if used.canuse():
		used.use()
	if used.current < 1:
		# if it's a one time Item like a potion it's deleted
		if used.renewable == 1:
			Item.query.filter_by(id=item).delete()
	db.session.commit()
	return redirect("/")

@app.route("/recharge", methods = ["GET","POST"])
@char_selected
def recharge():
	if request.method == "POST" and request.form['numCharge'] != "":
		charged = Item.query.filter_by(id=request.form['itemCharge']).first()
		charged.charge(request.form["numCharge"])
		db.session.commit()
	items = Item.query.filter_by(owner = g.character).filter_by(renewable = 2).all()
	return render_template("recharge.html",items=items)


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
@app.route("/rest")
@char_selected
def rest():
	items = Item.query.filter_by(owner = g.character).all()
	for item in items:
		item.rest()
	db.session.commit()
	return redirect("/")

@app.route("/a")
def tfun():
	chars = Character.query.all()
	for char in chars:
		print(char.name + ": " + str(char.id))
		spel = Spell.query.filter_by(parent_id=char.id).all()
		for spe in spel:
			print(spe.spellname)
		print("--------------")
	return "Results have been posted to logs :)  "

@app.route("/admin")
@char_selected
def adm():
	bdy = ""
	chars = Character.query.all()

	for char in chars:
		bdy += "<div class = 'card'>"
		bdy += char.name + ": (ID:" + str(char.id) + ") <a href = '/d/Character/" + str(char.id) + "'>Delete</a><br>"
		spel = Spell.query.filter_by(parent_id=char.id).all()
		ite = Item.query.filter_by(owner=char.id).all()
		bdy += "------------Spells:------------<br>"
		for spe in spel:
			bdy += spe.spellname + "<a href = '/d/Spell/" + str(spe.id) + "'>DELETE SPELL </a><br>"
		bdy += "------------ Items:------------<br>"
		for itme in ite:
			bdy += itme.name + "<a href = '/d/Item/" + str(itme.id) + "'>DELETE ITEM </a><br>"
		bdy +="</div><br>"
	return render_template("base.html",cnt=bdy)

@app.route("/d/<path:type>/<path:id>")
def dele(type,id):
	if type == "Character":
		Character.query.filter_by(id=id).delete()
	elif type =="Spell":
		Spell.query.filter_by(id=id).delete()
	elif type == "Item":
		Item.query.filter_by(id=id).delete()
	db.session.commit()
	return redirect('/admin')

if (__name__ == "__main__"):
	app.run()
