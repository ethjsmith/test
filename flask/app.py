from flask import Flask

app = Flask(__name__)
#url = "test"

@app.route("/")
def testfunc():
	return "this is a test boys"

@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
