import flask_login, hashlib, datetime, subprocess, os
from importlib import import_module
from flask import Flask, request, render_template, redirect, url_for, flash, Response, g, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
#from vanilla import db
from vanilla import db
#db = SQLAlchemy()

class User(UserMixin, db.Model):
    '''User database model, created by new user (name,password,email)'''
    __tablename__ = "User"
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
    '''Comment Database model, has more complicated foriegn keys, and so should only be created by the scripts attacked to the /?/? post route'''
    __tablename__ = "Comment"
    id= db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String())
    message = db.Column(db.String())
    poster = db.Column(db.Integer, db.ForeignKey('User.id'))
    postername = db.Column(db.String())
    date = db.Column(db.String())
    article = db.Column(db.Integer)
    def __init__(self,title,message,poster,postername,article):
        self.title = title
        self.message = message
        self.poster = poster
        self.postername = postername
        self.article = article
        self.date = datetime.date.today()


class Post(db.Model):
    __tablename__ = "Post"
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



def init_db():
    # creates a test database with some test articles
    db.drop_all()
    db.create_all()
    b = User(name='test',password='pass',email='test@b.c')
    a = User(name='ethan',password='password',email='a',permission=999)
    # add and save the users
    db.session.add(a)
    db.session.add(b)
    p1 = Post(topic="misc",title="Example Article",picture="/static/Pic.jpg",body="This is the body of the article, which accepts <i> HTML tags </i>")
    p2 = Post(topic="misc",title="Ex2",picture="/static/Pic.jpg",body="some random placeholder text here please")
    p3 = Post(topic="a new topic appears",title="Example Article",picture="/static/Pic.jpg",body="I yote a duck off a cliff... turns out they can fly, so everything was fine")

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.commit()

if __name__ == '__main__':
    init_db()
