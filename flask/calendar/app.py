from flask import Flask,request,redirect

app = Flask(__name__)
#url = "test"
tasks = []
complete = []
@app.route("/")
def testfunc():
	return "this is a test boys"

@app.route('/today', methods = ['GET','POST'])
def today():
		z = ""
		if request.method == 'POST':
			removeus = str(request.get_data()).replace("+"," ").split("&")
			print (removeus)
			for remove in removeus:
				r = remove[:-1].split("=")
				if r[1] in tasks:
					tasks.remove(r[1])
					complete.append(r[1])
					while len(complete) > 5:
						del complete[0]
			#print(removeus)
		for task in complete:
			z = z + "<div style='text-decoration:line-through;'>" + task + "</div><br>"
		for task in tasks:
			z = z + "<input type='checkbox' name='Task' value='"+ task +"'>"+ task +"<br>"
		#print(tasks)
		#print(complete)
		return """<html><body><h3> TODO </h3>
		<form action="/today" method="POST">""" + z + """<input type="submit" value="Submit">
		</form><form action="/today/a" method="POST"><input type = "text" name="task"><input type="submit" value="Add item"></form>
		</body></html>"""

@app.route("/today/a", methods = ['GET','POST'])
def additem():
	if request.method == 'POST':
		#print request.get_data()
		apendme = str(request.get_data()).replace("+"," ").split("=")
		tasks.append(apendme[1][:-1])
	return redirect('/today')

@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
