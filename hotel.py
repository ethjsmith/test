from flask import Flask
import mysql.connector
#from flaskext.mysql import MySQL
#app = Flask(__name__)
#app.config['mysql_database_host'] = 'localhost'
#app.config['mysql_database_port']= 3306
#app.config['mysql_database_db']='group_project'
#app.config['mysql_database_user']='root'

#mysql = MySQL()
#mysql.init_app(app)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port='3306'

)

print(db)
@app.route("/")
def login():
    return "something"
# requried : show hotels
@app.route("/hotels")
def data():
    c = mysql.get_db().cursor()
    c.execute("SELECT * FROM hotels;")
    z = c.fetchall()

    return z
# required : rooms in a hotel :L
@app.route("/rooms")
def rooms():
    return "something"
# required : some reservations
@app.route("/reservations")
def reservations():
    return "something "


if (__name__ == "__main__"):
  app.run()
