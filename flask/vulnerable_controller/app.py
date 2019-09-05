import flask_login, hashlib, datetime, subprocess,pycamera,time
#from flask import Flask,current_ap,g
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# all this first bit is mostly boilerplate that lets the server run, it's not really interesting
# although I guess you can see how users are stored, and how admin is determined

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# this class corelates with a table in a database, the variables each become attributes
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    # this is an interesting attribute, I wonder how it works ?
    is_admin = db.Column(db.Integer)
    def __init__(self,name,password,is_admin):
        self.name = name
        self.password = password
        self.is_admin = is_admin
    def is_active(self):
        return True
    def is_user(self):
        return False
    def is_authenticated(self):
        return True

class NotUser(AnonymousUserMixin):
    name = u"Not Logged In"

app.secret_key='9'
login_manager = LoginManager()
login_manager.anonymous_user = NotUser
login_manager.login_view = "login"
login_manager.login_message = u'Please Log in'
login_manager.refresh_view = "reauth"
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
login_manager.setup_app(app)
#
#   \/ Interesting stuff mostly starts here \/
#
# this is the main homepage, which doesn't really do anything

# how flask works :
# @app.route() <-- this is the url for a portion of the website
#@login_required <-- this is a requirement. it means a user has to be logged in to see the page
# def something(): <-- this is the function that runs when the user accesses the page
# logic in here runs whenever a user accesses a page
#   Return x <-- the return of the function is what the webpage shows to the users. render_template(x) generates a nice looking webpage but is the same idea


@app.route("/")
def homepage():
    return render_template("genericpage.html",body="welcome to the controller website")
# this is the login
@app.route("/login", methods=["GET","POST"])
def login():
    # if you're already logged in, then you just go back to the homepage
    if current_user.name != "Not Logged In":
        return redirect("/")
    # if you submitted a login query you come here, where it checks if your info is correct
    if request.method == "POST" and "username" in request.form:
        # if you make the same username as somebody else looks like you wont be able to log in... I should fix this
        user = User.query.filter_by(name=request.form["username"]).first()
        if user != None:
            #print(user)
            # cheks if the entered username and password match what is in the database.
            username = request.form["username"]
            passw = request.form["password"]
            if username == user.name and passw == user.password:
                print("successful login for " + username)
                if login_user(user,remember=True):
                    flash("successful login")
                    print(current_user.name,current_user.password,current_user.is_admin)
                    return redirect("/")
        print('login failed lol noob')
        # if you fail to login ( enter the wrong info) the program ends up here and basically reloads the login page
        flash("login failed!")
        return redirect("/login")
    # if you are coming to the login page for the first time, you skip all the logic and end up here
    return render_template("login.html")
# this method lets people register for accounts if they are new to the site
@app.route('/register', methods=["GET","POST"])
def register():
    if current_user.name != "Not Logged In":
        flash("must be logged out to create a new user")
        return redirect("/")
    if request.method == "POST":
        if 'name' in request.form and 'password' in request.form:
            # anyone who has "king" in their username is a level 2 admin lol just testing, Ill fix this later
            if "king" in request.form['name']:
                a = User(request.form['name'],request.form['password'],2)
            else:
                a = User(request.form['name'],request.form['password'],0)
            db.session.add(a)
            db.session.commit()
            flash("new user registered")
            return redirect("/")

    return render_template("register.html")

# this route logs users out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out!')
    return redirect('/')

# here's a control for low level admins to control X
@app.route('/control')
@login_required
def control():
    if current_user.is_admin >= 1:
        return render_template('genericpage.html',body="hack page lol")
    else:
        flash ("you have to be a logged in admin to acces this page!")
        return redirect("/")

# this page lets you search the database for usernames... (maybe )
@app.route('/data')
@login_required
def data():
    if current_user.is_admin >= 2:
        print("in progress")
    else:
        flash("you have to be a level 2 admin to access this page!")
        return redirect("/")

# this page checks to make sure a user is an admin before sending them on to the control page for speaker
@app.route('/speaker')
@login_required
def speak():
    if current_user.is_admin >= 3:
        return redirect("/speakerControl")
    else:
        flash("you must be a level 3 admin to access this page!")
        return redirect("/")
# this is the actual control page for the speaker !
@app.route("/speakerControl", methods=["GET","POST"])
def speak2():
    if request.method == "POST" and 'words' in request.form:
        command = 'espeak ' + '"' + request.form['words'] + '"'
        subprocess.call(["/usr/bin/espeak", request.form["words"]])

    return render_template("speak.html")
# the piece of the function that runs the webserver

@app.route('/camera/<path:adminid>')
@login_required
def cam(adminid):
    if int(adminid) >= 4:
        subprocess.call(["python3", "/home/pi/test/flask/vulnerable_controller/cam.py"])
        return render_template("genericpage.html", body="<img src='pic.jpg'>")
    else:
        flash("you must be a level 4 admin to access this page !")
        return redirect("/")
    #f current_user.is_admin >= 4:
    #experimental new login system
    #print(adminid)

if (__name__=="__main__"):
    app.run()
