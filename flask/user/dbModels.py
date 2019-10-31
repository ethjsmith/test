import datetime
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#from vanilla import ap

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    comments = db.relationship('Comment', backref ='usr', lazy='dynamic', primaryjoin="User.id == Comment.poster")

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

# allows modification of user accounts
    def change_name(self, name):
        self.name = name
    def change_email(self,email):
        self.email = email
    def change_password(self,password):
        self.password = self.set_password(password)

class Comment(db.Model):
    __tablename__ = "comments"
    id= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String())
    message = db.Column(db.String())
    # it would be better if poster was a forigen key, but this works for now
    #poster = db.column(db.Integer, db.ForeignKey('User.name')
    #poster = db.relationship('User')
    poster = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.String())
    article = db.Column(db.Integer)
    def __init__(self,title,message,poster,article):
        self.title = title
        self.message = message
        self.poster = poster
        self.article = article
        self.date = datetime.date.today()


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String())
    title = db.Column(db.String())
    picture = db.Column(db.String())
    body = db.Column(db.String())
    para = db.Column(db.String())
    date = db.Column(db.String())
    def __init__(self,topic,title,picture,body):
        self.topic = topic
        self.title = title
        self.picture = picture
        self.body = body
        self.getFirstParagraph()

    def getFirstParagraph(self):
        self.para = str(self.body.split("</p>")[0])

class Anon(AnonymousUserMixin):
    name = u"Not Logged in"
