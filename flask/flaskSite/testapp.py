from flask import Flask
from flask_basicauth import BasicAuth
import os
import configure


app = Flask(__name__,static_url_path="",static_folder='/home/ejsmith/Documents/test/flaskSite/')

style = '''<html><head>
<link rel = "stylesheet" href="style.css">
</head></html>'''
header = '''
<html>
	<head><title>Template topbar</title></head>
</html>'''
coolthing = '''<html><body> Welcome to the site</body></html>'''
@app.route('/')
def site():
	return '''
<html>
	<head>
		<title>Test site</title>
	</head>
	<body>
		<h1> Welcome to the site </h1>
	</body>
</html>'''

@app.route('/test')
def test():
	return header + style  + coolthing + '''<html>
<body> <p>This is a test body paragraph<p>  </body>

</html>'''



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
