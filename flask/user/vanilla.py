import sqlite3, flask_login
#from flask import Flask,current_app,g
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)



#url = "test"
class User(UserMixin):
		def __init__(self,name,id,passwd,active=True):
			self.name = name
			self.id = id
			self.active = active
			self.passwd = passwd

		def is_active(self):
			# check if is_active
			return self.active
		def is_user(self):
			return False
		def is_authenticated(self):
			return True

class Anon(AnonymousUserMixin):
	name = u"Anon"

# temporary stuff
USERS = {
	1: User(u"ejsmith",1,"password"),
	2: User(u"bob",2,"memes"),
	3: User(u"test",3,"yes"),
}
USER_NAMES = dict((u.name, u) for u in USERS.values())

app = Flask(__name__)
app.secret_key = "8888888888888888888888888888888888"

login_manager = LoginManager()
login_manager.anonymous_user = Anon
login_manager.login_view = "login"
login_manager.login_message = u"Please log in"
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
	return USERS.get(int(id))

login_manager.setup_app(app)

@app.route("/")
def testfunc():
	return "this is a test boys"

@app.route("/<path:url>")
@fresh_login_required
def test2(url):
	return "your url is " + url

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "POST" and "username" in request.form:
		username = request.form["username"]
		if username in USER_NAMES:
			remember = request.form.get("rememeber", "no") == "yes"
			if login_user(USER_NAMES[username], remember=remember):
				flash("logged in!")
				return redirect(request.args.get("next") or "/")
			else:
				flash("false creds")
		else:
			flash(u"invalid username")
	return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("logged out")
	return redirect("/")

if (__name__ == "__main__"):
	app.run()

#return '<html>' + stylesheet + templ.header(0) +
#'<h1> File share </h1> <div class = \"card\">
#<form method = \"POST\" enctype = \"multipart/form-data\"><input type = \"file\" name = \"file\" />
#<input type = \"submit\" value = \"upload file\"/></form></div><br><div class = \"card\">' + links + '
#</div></html>'
