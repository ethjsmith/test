from flask import Flask,request,redirect
from werkzeug import secure_filename
import os


# this is a file for proof of concept of uploading and downloading files to a flask website
# probably you should also add basic authentication, or else anyone could add, or delete anything from this page 




#app = Flask(__name__,static_url_path="",static_folder='/home/ejsmith/Documents/test/flaskSite/')

app = Flask(__name__,static_url_path="",static_folder='/home/ejsmith/Documents/test/flask/fileshare/')
#url = "test"

@app.route("/files", methods = ['GET','POST'])
def testfunc():
	if request.method == 'POST':
		f = request.files['file']
		f.save('uploads/' + secure_filename(f.filename))
	content ="""
<form action = "http://localhost:5000/files" method = "POST" enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
</form><br>
"""
	filez = os.listdir('uploads/')
	for fi in filez:
		content = content + "<a href = \"uploads/" + fi + "\" >" + fi + "</a>"
		content = content + "<form action=\"uploads/d/" + fi + "\" method = \"get\" target=\"blank\"> <button type = \"submit\" >Delete " + fi + "</button></form><br>"
		print fi
#onclick = \"window.location.href =uploads/d/" + fi + "\" >Delete" + fi + "</button><br>"
	all = "<html><body>" + content + "</body></html>"
	return all
# this special route deletes the file instead of returning it ... very fancy 
@app.route("/uploads/d/<path:filename>")
def deletefile(filename):
	if os.path.exists('uploads/' + filename):
		os.remove('uploads/' + filename)
	return redirect('/files')
@app.route("/<path:url>")
def test2(url):
	return "your url is " + url

if (__name__ == "__main__"):
	app.run()
