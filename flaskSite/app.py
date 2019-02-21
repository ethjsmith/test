from flask import Flask
from flask_basicauth import BasicAuth
import os


app = Flask(__name__,static_url_path="",static_folder='/home/ejsmith/Documents/test/flaskSite/')

app.config['BASIC_AUTH_USERNAME'] = os.environ['user']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['pass']

basic_auth = BasicAuth(app)

@app.route('/admin')
@basic_auth.required
def admin():
	return app.send_static_file('admin.html')
@app.route('/')
def site():
	return app.send_static_file('index.html')

@app.route('/secret')
@basic_auth.required
def secret():
	return app.send_static_file('secret.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
