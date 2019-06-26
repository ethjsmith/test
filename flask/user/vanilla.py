import flask_login, hashlib
#from flask import Flask,current_app,g
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self,name,password,email):
        self.name = name
        self.password = password
        self.email = email
    def is_active(self):
        return True
    def is_user(self):
        return False
    def is_authenticated(self):
        return True

class Anon(AnonymousUserMixin):
	name = u"Not Logged in"

app.secret_key = "x9fLx81af*x90xbfx03xfaBxfcxc9r)x84x8bxd1xcafxe92x08x99x1exee8x05nt"
login_manager = LoginManager()
login_manager.anonymous_user = Anon
login_manager.login_view = "login"
login_manager.login_message = u"Please log in"
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_manager.setup_app(app)

@app.route("/")
def testfunc():
	return "user:" + current_user.name

@app.route("/<path:url>")
@fresh_login_required
def test2(url):
	return "user:" + current_user.name + " & your url is " + url

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        user = User.query.filter_by(email=request.form["username"]).first()
        print(user)
        username = request.form["username"]
        pas = request.form["password"]
        print(username)
        print(pas)
        print("=====")
        #usr.name = username
        #usr.id = 1
        #usr.passwd = pas
        if username  == user.email:
            print("username is in USER_NAMES")
            if pas == user.password:
            #if pas  == USER_NAMES[username].password:
                print("good password")
                #USER_NAMES[username].authed = True
                #user
                if login_user(user,remember=True):
                    print("successful login for " + user.name)
                    return redirect("/")
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
