import flask_login, hashlib, datetime

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUserMixin, confirm_login, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

ap = Flask(__name__)
ap.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
ap.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(ap)

class item(db.Model):
    __tablename__ = 'items'
    id= db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String())
    isKey = db.Column(db.Integer)
    def __init__(self,name,isKey):
        self.name = name
        self.iskey = isKey

class key(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String())
    def __init__(self,name):
        self.name = name
ap.secret_key = "69"
def searchbar():
    return '''<form method = "POST" enctype = "multipart/form-data">
        <input type = "text" name = "q" placeholder = 'item name'/>
        <input type = "submit" value = "search"/>
    </form>'''
@ap.route("/", methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        if q in request.form:
            z = item.query.order_by(id = request.form['q']).all()
            x =""
            for zz in z:
                x += str(zz.name)
            return searchbar() + "stuff<br>" + x
    z = item.query.order_by(item.id,isKey=0).all()
    x =""
    for zz in z:
        x += str(zz.name)
    return searchbar() + "stuff<br>" + x

if (__name__ == "__main__"):
    ap.run()
