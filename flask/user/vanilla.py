import sqlite3, flask_login, hashlib, sqlalchemy
#from flask import Flask,current_app,g
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)



#url = "test"
class User(UserMixin):
        def __init__(self,name,passwd,id,active=True):
            self.name = name
            self.id = id
            self.active = active
            self.passwd = passwd
            self.authed = False

        def is_active(self):
			# check if is_active
            return self.active
        def is_user(self):
            return False
        def is_authenticated(self):
            return authed

class Anon(AnonymousUserMixin):
	name = u"Anon"

# temporary stuff
USERS = {
	1: User(u"ejsmith","password",1),
	2: User(u"bob","memes",2),
	3: User(u"test","yes",3),
}
USER_NAMES = dict((u.name, u) for u in USERS.values())

#accounts2 = [
#    ["ejsmith","password","0"],
#    ["bob","memes","1"],
#    ["test","yes","2"]
#]

#accounts = {
#    1: User("ejsmith","password",0),
#    2: User("bob","meme",1),
#    3: User("test","yes",2),
#}
#account_names = dict()

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
#    if accounts[id][2] == id:
#        user = User(accounts[id][0],accounts[id][1],accounts[id][2])
#        return user
#    else:
#        return
#    return accounts.get(int(id))
    #return accounts[id]
login_manager.setup_app(app)

@app.route("/")
def testfunc():
	return "user:" + current_user.name

@app.route("/<path:url>")
@fresh_login_required
def test2(url):
	return "user:" + current_user.name + " & your url is " + url

@app.route("/login", methods=["GET","POST"])
# def login():
#	if request.method == "POST" and "username" in request.form:
#		username = request.form["username"]
#		if username in USER_NAMES:
#			remember = request.form.get("rememeber", "no") == "yes"
#			if login_user(USER_NAMES[username], remember=remember):
#				flash("logged in!")
#				return redirect(request.args.get("next") or "/")
#			else:
#				flash("false creds")
#		else:
#			flash(u"invalid username")
#	return render_template("login.html")
# better login?
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        pas = request.form["password"]
        print(username)
        print(pas)
        print("=====")
        #usr.name = username
        #usr.id = 1
        #usr.passwd = pas
        if username in USER_NAMES:
            print("username is in USER_NAMES")
            if pas  == USER_NAMES[username].passwd:
                print("good password")
                USER_NAMES[username].authed = True
                if login_user(USER_NAMES[username]):
                    print("successful login")
                    return redirect("/")


        #if username in accounts:
        #for users in accounts:
        #    if username == users.name:
        #        if pas == users.passwd:
        #            login_user(users)
        #            return redirect(request.args.get("next") or "/")
        #        return "wrong password"
        #return "wrong username"
    #else:
    #    return "bad login"
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
