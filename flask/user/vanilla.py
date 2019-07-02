
import flask_login, hashlib
#from flask import Flask,current_app,g
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String())
    title = db.Column(db.String())
    picture = db.Column(db.String())
    body = db.Column(db.String())

    def __init__(self,topic,title,picture,body):
        self.topic = topic
        self.title = title
        self.picture = picture
        self.body = body

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self,name,password,email):
        self.name = name
        self.password = self.set_password(password)
        self.email = email
    def is_active(self):
        return True
    def is_user(self):
        return False
    def is_authenticated(self):
        return True
    # save password as a hash instead of plaintext
    def set_password(self,password):
        return generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)

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
    z = "user:" + current_user.name
    return render_template('genericpage.html',title="home",body="Welcome to the homepage")


	#return "user:" + current_user.name + " & your url is " + url

@app.route('/register', methods=["GET","POST"])
def register():
    if current_user.name != "Not Logged in":
        return redirect ("/mypage")
    if request.method == 'POST':
        print(request.form['name'],request.form['password'],request.form['email'])
        if 'name' in request.form and 'password' in request.form and 'email' in request.form:
            if request.form['password'] == request.form['password2']:
                new = User(request.form['name'],request.form['password'],request.form['email'])
                db.session.add(new)
                db.session.commit()
                return "new user added "
    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.name != "Not Logged in":
        return redirect("/mypage")
    if request.method == "POST" and "username" in request.form:
        user = User.query.filter_by(email=request.form["username"]).first()
        if user != None:
            print(user)
            username = request.form["username"]
            pas = request.form["password"]
            print(username)
            print(pas)
            print("=====")
            if username  == user.email:
                print("username is an email")
                if user.check_password(pas):
                #if pas == user.password:
                    print("good password")
                    if login_user(user,remember=True):
                        print("successful login for " + user.name)
                        flash("successful login for " + user.name,"notify")
                        return redirect(request.args.get("next") or "/")
                        #return redirect("/")
        flash("login failed, wrong username(email) or password","alert")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("logged out")
	return redirect("/")

@app.route('/admin')
@login_required
def admin():
    p = ""
    # High security admin page
    if current_user.email != 'a':
        return redirect('/mypage')
    all = User.query.all()
    for usr in all:
        p += "name:" + usr.name + ", email:" + usr.email + "<br>"
    #return "hello master<br><br>" + p
    return render_template("genericpage.html",title='admin',body=p)
@app.route('/mypage')
@login_required
def userpage():
    return render_template("genericpage.html", body=current_user.name +":"+ current_user.email + "This is where you will be able to change your details bruh")
    # a form for changing uname and/or pword
    z = ""

@app.route("/<path:url>")
def test2(url):
    #user = User.query.filter_by(email=request.form["username"]).first()
    posts = Post.query.filter_by(topic=url).all()
    if posts:
        x = ""
        for post in posts:
            x += post.title + ":" + str(post.id) + "<br>"
        return render_template("genericpage.html", body = x,title = url)
    return render_template("genericpage.html",body="Topic not found!",title="Error")
#    return render_template('genericpage.html',title=url,body=url)
@app.route("/<path:url>/<path:url2>")
def rtcle(url,url2):
    post = Post.query.filter_by(topic=url,id=url2).first()
    if post:
        return render_template("article.html",article_image=post.picture,article_title=post.title,article_body=post.body)
    return render_template("genericpage.html",body="Article not found!",title="Error")

if (__name__ == "__main__"):
	app.run()

#return '<html>' + stylesheet + templ.header(0) +
#'<h1> File share </h1> <div class = \"card\">
#<form method = \"POST\" enctype = \"multipart/form-data\"><input type = \"file\" name = \"file\" />
#<input type = \"submit\" value = \"upload file\"/></form></div><br><div class = \"card\">' + links + '
#</div></html>'
