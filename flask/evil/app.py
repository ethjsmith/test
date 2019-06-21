from flask import Flask, send_file, request

app = Flask(__name__)
#url = "test"

@app.route("/")
def testfunc():
	print request.headers.get("User-Agent")
	try:
		return send_file('lesser.sh')
	except Exception as e:
		return str(e)

@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
