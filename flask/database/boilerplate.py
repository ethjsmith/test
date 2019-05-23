import sqlite3

# This file is used to test writing to a database... the password is fake, as is all of the data, obvs lel
dbfile = '/home/users/ejsmith/Documents/test/flask/database/newdata.sqlite'
dbfile2 = 'data3.sqlite'
dbfile3 = 'newdata.sqlite'

conn = sqlite3.connect(dbfile3)

c = conn.cursor()

def createDB():
    with open('schema2.sql') as f:
        c.executescript(f.read())
def insertIntoTable(data,table,field):
    c.execute("INSERT OR REPLACE INTO {table_} ({field_}) VALUES ({data_});".format(table_=table,field_=field,data_=data))
def getTable(table):
    c.execute("SELECT * FROM {table_}".format(table_=table))
    print(c.fetchall())
#createDB()
insertIntoTable('"172.2.3.4"','ip_addresses','address')
getTable('ip_addresses')
getTable('correlations')
conn.commit()
conn.close()
