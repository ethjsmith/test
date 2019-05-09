from flask import Flask,request,redirect

# test how variables can be passed around in POST requests, to possibly simplify how my webserver works
#improving the webserver seems to be a common theme of this folder of test projects

app = Flask(__name__)
#url = "test"
# basic test of reading argument variables
light = 1
@app.route("/a",methods = ['GET','POST'])
def send():
	if request.args.get('arg1') is None:
		return "no arg1 provided"
	return request.args.get('arg1')

#More advanced implimentation
@app.route("/")
def vartest():
# the variables are named weird because I was testing if they're names mattered and no it seems not lol
# the problem I ended up trying to troubleshoot was caused because I was testing in python 2.7 and running in 3.4 pepega
	if request.args.get('arzzg2') is not None:
		changelight(request.args.get('arzzg2'))
	return '<html><body>' + str(light) + '<br><a href = "/?arzzg2=yes">Change light</a></body></html>'

# this might be the crappiest code I've ever written lol
def changelight(do):
	global light
	if do == 'yes':
		if light == 1:
			light = 0
		else:
			light = 1
	print light
	return
# leftovers from the template
@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
