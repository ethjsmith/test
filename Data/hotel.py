#Author Ethan Smith

from flask import Flask, render_template
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="ejsmith",
    password="password",
    auth_plugin='mysql_native_password',
    database="group_project",
    port='3306'
)
app = Flask(__name__)
print(db)#debugging
c = db.cursor()
@app.route("/")
def homepage():
    return render_template("main.html")
# requried : show hotels
@app.route("/hotels")
def data():
    c.execute ("describe hotel;")
    z = c.fetchall()
    tableheadings = []
    for x in z:
        print(x[0])
        tableheadings.append(x[0])
    c.execute("SELECT * FROM hotel;")
    content = c.fetchall()

    return render_template('table.html',tableheadings=tableheadings,content=content)
# required : rooms in a hotel :L
@app.route("/rooms")
def rooms():
    c.execute ("describe rooms;")
    z = c.fetchall()
    tableheadings = []
    for x in z:
        print(x[0])
        tableheadings.append(x[0])
    c.execute("select * from rooms")
    content = c.fetchall()
    return render_template('table.html',tableheadings=tableheadings,content=content)
# required : some reservations
@app.route("/reservations")
def reservations():
    c.execute ("describe reservation;")
    z = c.fetchall()
    tableheadings = []
    for x in z:
        print(x[0])
        tableheadings.append(x[0])
    c.execute("select * from reservation")
    content = c.fetchall()
    return render_template('table.html',tableheadings=tableheadings,content=content)


if (__name__ == "__main__"):
  app.run()
