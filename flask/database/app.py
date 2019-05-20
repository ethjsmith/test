import sqlite3

from flask import Flask,current_app,g
from flask.cli import with_appcontext

app = Flask(__name__)
app.config['DATABASE'] = 'data.sqlite'
#url = "test"

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db
def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	db = get_db()
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))



@app.route("/")
def testfunc():
	return "this is a test boys"

@app.route("/db")
def datatest():
	init_db()
	return 'testing'
@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()