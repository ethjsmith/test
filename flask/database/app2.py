import sqlite3

# This file is used to test writing to a database... the password is fake, as is all of the data, obvs lel
dbfile = '/home/users/ejsmith/Documents/test/flask/database/data2.sqlite'
dbfile2 = 'data3.sqlite'
dbfile3 = 'data.sqlite'
conn = sqlite3.connect(dbfile3)
c = conn.cursor()

def createtable():
    c.execute('CREATE TABLE {name} ({field} {type})'.format(name="table_of_names",field="Names",type="TEXT"))

def addthing(thing,passw):
    c.execute("SELECT * FROM user ORDER BY id DESC LIMIT 1;")
    z = c.fetchone()
    if z==None:
        z = 0
    else:
        z = z[0]
    z+=1
    print(z)
    c.execute("INSERT INTO user (id,username,password) VALUES('{id}','{th}','{ps}');".format(id=z,th=thing,ps=passw))

def selectall():
    c.execute('SELECT * FROM {name}'.format(name='user'))
    mydata = c.fetchall()
    print(mydata)
def removething(thng):
    c.execute("DELETE FROM user WHERE id={tng};".format(tng=thng))

def gameloop():
    selectall()
    print("1: add something")
    print("2: delete something")
    print("3: quit")
    userin = input("choose a number")
    if (userin == 1):
        add()
    elif (userin == 2):
        dele()
    else:
        return False
    return True

def add():

    v1 = raw_input("enter your name: ")
    v2 = raw_input("Enter a passworkd: ")#intentional?
    addthing(v1,v2)
    conn.commit()
def dele():
    # this is bad because it crashes if you add a number OMEGALUL
    vv = input("Delete an index?")
    removething(vv)
    conn.commit()
def doit():
    c.execute("SELECT * FROM correlations;")
    mydata = c.fetchall()
    print(mydata)

#selectall()
#z = True
#while z == True:
#    z = gameloop()
doit()
conn.commit()
conn.close()
