
import flask_login, hashlib, datetime
from importlib import import_module
from flask import Flask, request, render_template, redirect, url_for, flash, Response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
#Camera = import_module('camera_pi').Camera
from dbModels import db, Anon, Comment, Post, User
ap = Flask(__name__)
ap.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
ap.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(ap)

# this seems like something that should be hidden lol
ap.secret_key = "x9fLx81af*x90xbfx03xfaBxfcxc9r)x84x8bxd1xcafxe92x08x99x1exee8x05nt"
login_manager = LoginManager()
login_manager.anonymous_user = Anon
login_manager.login_view = "login"
login_manager.login_message = u"Please log in"
login_manager.refresh_view = "reauth"
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_manager.setup_app(ap)
def get_topics():
    topics = Post.query.with_entities(Post.topic).distinct()
    return topics

def gen(camera):
# generates video stream
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def is_admin():
    if current_user.email != 'a':
        return True
    return False

def get_posts():
    #(title)
    z = Post.query.all()
    return z
def get_comments(z):
    comments = Comment.query.filter_by(article=z)
    return comments


@ap.route("/")
def testfunc():
    z = "user:" + current_user.name
    if isinstance(current_user,Anon):
        z += "<br>is anon"
    return render_template('genericpage.html',title="home",body="Welcome to the homepage",topics=get_topics())

@ap.route('/About')
def about_page():
    k = "<h1>About Me</h1><br><p>My name is Ethan Smith, and I am a CSIS student at Southern Utah University. at SUU I am also the Vice President of the cyber defence (competition) club, and a student security analyst. I love programming ( prefer Python and Java), Snowboarding during the winter, and playing lots of different video games. I also enjoy homemade IOT devices, and <br> Contact me at `ethan@esmithy.net` </p> <p> About the site: <br> This site was built as a project, just something that I like to play around with when I have some downtime between work and school. I had the idea to make a website which instead of having static html files and PHP templates, would use python to generate all the pages by chaining together string variables containing bits of html, which altogether would generate web pages. I've done a lot of things to try and make the site scalable, instead of static, and I've really enjoyed putting it together, although writing html with python syntax highlighting can be a pain sometimes! </p>"
    return render_template('genericpage.html',title="About",body=k,topics=get_topics())
    #return "user:" + current_user.name + " & your url is " + url

@ap.route('/register', methods=["GET","POST"])
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
                flash("New user added")
                return redirect('/login')
    return render_template("register.html",topics=get_topics())


@ap.route("/login", methods=["GET","POST"])
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
    return render_template("login.html",topics=get_topics())

@ap.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out")
    return redirect("/")

@ap.route('/control')
@login_required
def control():
    if is_admin():
        return redirect("/mypage")
    bdy = "<a href='/control/go?arg=on'>Light On</a><br><a href='/control/go?arg=off'>Light Off</a><br><a href='/control/go?arg=on1'>Fan On(This doesnt do anything)</a><br><a href='/control/go?arg=off1'>Fan Off( This ones doesn\'t either lol)</a><br></p>"
    return render_template("genericpage.html",body=bdy,topics=get_topics())

@ap.route('/control/go')
@login_required
def doEverything():
    if is_admin():
        return redirect("/mypage")
    if request.args.get('arg') != None:
        if request.args.get('arg') == "on":
            print("do thing 1")
            #subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[1]])
        elif request.args.get('arg') == "off":
            print("do thing 2")
            #subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[2]])
        elif request.args.get('arg') == "on1":
            print("do thing 3")
            #subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[3]])
        elif request.args.get('arg') == "off1":
            print("do thing 4")
            #subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[4]])
        else:
            print ("error?")
    return redirect('/control')

# this route is the actual video stream, the next one shows it 
@ap.route('/video')
@login_required
def video():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@ap.route('/vid')
@login_required
# displays the video with other website contents
def vid():
    return render_template('stream.html')


@ap.route('/admin')
@login_required
def admin():
    if is_admin():
        return redirect('/mypage')
    # High security admin page
    users = User.query.all()
    return render_template("admin.html",title='admin',topics=get_topics(),users=users,pages=get_posts())


# admin delete driver, used for deleting any kind of content on the site
@ap.route('/admin/<path:type>/<path:did>')
@login_required
def admin_delete(type,did):
    #todo : add a check that delets any comments related to a user before delting them ( or changes the primary key or smth)
    if is_admin():
        if type == 'comment':
            return redirect('/deletecomment/' + did)
        return redirect('/mypage')
    if type == "page":
        Post.query.filter_by(title=did).delete()
    elif type == "user":
        User.query.filter_by(email=did).delete()
    elif type == "comment":
        Comment.query.filter_by(id=did).delete()
    else :
        print("error lol")
    db.session.commit()
    return redirect(request.referrer or '/admin')


# a delete function for users to delete their own comments
@ap.route('/deletecomment/<path:cid>')
@login_required
def user_delete_comment(cid):
    e = Comment.query.filter_by(id=cid).first()
    if e.poster == current_user.name:
        nextd = Post.query.filter_by(id=e.article).first()
        db.session.delete(e)
        db.session.commit()
        return redirect('/' + nextd.topic + '/' + str(nextd.id))
    return redirect('/')


#This page is for a user to modify their own account
@ap.route('/mypage', methods=["GET","POST"])
@login_required
def userpage():
    if request.method == "POST":

        if request.form['username'] != '':
            flash("username updated")
            zz = Comment.query.all()
            #zz = Comment.query.filter_by(poster="dog").all()
            #print(zz)
            for z in zz:
                #update the username
                print(z)
                print(z.poster)
                z.poster = request.form['username']
            current_user.name = request.form['username']

        if request.form['password'] != '':
            if request.form['password'] == request.form['password2']:
                flash("password updated")
                current_user.change_password(request.form["password"])
            else:
                flash("Error, passwords don't match")
        if request.form['email'] != '':
            q= db.session.query(User.id).filter_by(email=request.form['email']).first()
            if q is not None:
                flash('error, invalid email( or already in use)')
            else:
                current_user.email = request.form['email']
                flash("Email updated")
        db.session.commit()

    return render_template('userManage.html', topics=get_topics())
    #return render_template("genericpage.html", body=current_user.name +" : "+ current_user.email + "<br>This is where you will be able to update your account if I ever get around to programming this section :) ",topics=get_topics())
    # a form for changing uname and/or pword
    z = ""


#This section is the driver for all headings
@ap.route("/<path:url>")
def topic(url):
    print(request.path)
    #user = User.query.filter_by(email=request.form["username"]).first()
    posts = Post.query.filter_by(topic=url).all()
    if posts:
        x = ""
        for post in posts:
            x += post.title + ":" + str(post.id) + "<br>"
        return render_template("list.html",title = url, topics = get_topics(), articles = posts)
    return render_template("genericpage.html",body="Topic not found!",title="Error",topics=get_topics())


# This section is the driver for all generic article pages
@ap.route("/<path:url>/<path:url2>",methods=["GET","POST"])
def artcle(url,url2):
    if request.method == "POST": #and "username" in request.form:
        if 'title' in request.form and 'message' in request.form:
            # logic for add comment
            z = Comment(title=request.form['title'],message=request.form['message'],poster=current_user.name,article=url2)
            db.session.add(z)
            db.session.commit()
    post = Post.query.filter_by(topic=url,id=url2).first()
    if post:
        return render_template("article.html",art = post,topics=get_topics(),title=post.title,comments=get_comments(post.id))
    return render_template("genericpage.html",body="Article not found!",title="Error",topics=get_topics())




if (__name__ == "__main__"):
    ap.run()
