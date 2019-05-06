from flask import Flask,request
from werkzeug import secure_filename
import os



#app = Flask(__name__,static_url_path="",static_folder='/home/ejsmith/Documents/test/flaskSite/')

app = Flask(__name__,static_url_path="",static_folder='/home/ejsmith/Documents/test/fileshare/')
#url = "test"

@app.route("/", methods = ['GET','POST'])
def testfunc():
	if request.method == 'POST':
		f = request.files['file']
		f.save('./uploads/' + secure_filename(f.filename))
	content ="""
<form action = "http://localhost:5000/" method = "POST" enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
</form>
"""
	filez = os.listdir('uploads/')
	for fi in filez:
		content = content + "<a href = \"uploads/" + fi + "\" >" + fi + "</a><br>"
	all = "<html><body>" + content + "</body></html>"
	return all

@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
