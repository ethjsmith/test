#Author Ethan Smith

from flask import Flask, render_template, redirect,request
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
# a method that will generate the data of generic pages
def genpage(ttable, tatribute=1,tvalue=1):
    c.execute("describe " + ttable)
    z = c.fetchall()
    tableheadings = []
    for x in z:
        tableheadings.append(x[0])
    c.execute("SELECT * FROM " + str(ttable) + " where " + str(tatribute) + " = \"" + str(tvalue) + "\";")
    content = c.fetchall()
    return content,tableheadings

@app.route("/")
def homepage():
    return render_template("main.html",stuff="Welcome to the homepage")

@app.route("/insert", methods=["GET","POST"])
def insert():
    if request.method == "POST":
        return redirect("/insert/" + request.form["table"])
    else:
        c.execute('show tables;')
        #anybody know anything about naming variables descriptive names? not me :)
        z = c.fetchall()
        print(z)
        zzz = []
        for zz in z:
            zzz.append(zz[0])
        z = zzz
        print (zzz)
        return render_template('insert.html', content = z)
# this method actually does the inserting :)
@app.route("/insert/<path:tbl>", methods=["GET","POST"])
def ins(tbl):
    if request.method == "POST":
        query = "insert into " + str(tbl) + " values ("
        for thing in request.form:
            query += "\"" + request.form[thing] + "\", "
        query = query[:-2] + ");"
        print(query)
        #return ":)"TESTING
        try:
            c.execute(query)
            db.commit()
            return render_template("main.html",stuff="Successfully added new record")
        except:
            return render_template("main.html",stuff="There was an error with the syntax of one of your entries :( ")
    else:
        c.execute('describe ' + tbl)
        z = c.fetchall()
        zzz= []
        for zz in z:
            zzz.append((zz[0],zz[1]))
        z = zzz
        return render_template('insert2.html',content = z)

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method =="POST":
        try:
            c.execute("describe " + request.form['table'])
            z = c.fetchall()
            tableheadings = []
            for x in z:
                tableheadings.append(x[0])
            c.execute("SELECT * FROM " + request.form['table'] + " where " +request.form['atribute']+ " = \"" + request.form['value'] + "\";")
            content = c.fetchall()

            return render_template('table.html',tableheadings=tableheadings,content=content)
        except:
            # hahaha this is the most trash thing I've ever done right here :^)
            tableheadings = ["nothing Found",]
            content =""
            return render_template('table.html',tableheadings=tableheadings,content=content)
    else:
        return render_template("search.html")
# required : show hotels and their managers
@app.route("/hotelManager")
def hotMan():
    return render_template("main.html")



# requried : show tables
# no way to sort these tho
@app.route("/s/<path:page>")
def generic(page):
    c.execute('show tables;')
            #anybody know anything about naming variables descriptive names? not me :)
    z = c.fetchall()
    print(z)
    xx = []
    for zz in z:
        xx.append(zz[0])
    print(xx)
    if (page in xx):
        ct = genpage(page)
        return render_template("table.html",tableheadings=ct[1],content=ct[0])
    else:
        return redirect("/")

if (__name__ == "__main__"):
  app.run()
