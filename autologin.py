import requests
login_url = 'http://localhost:5000/login'
next_url = 'http://localhost:5000/control/go?arg=on'
auth = {
    'username':'a',
    'password':'pass'
}
with requests.Session() as session:
    post = session.post(login_url, data=auth)
    r = session.get(next_url)
    #print(r.text)

# this script functions as a replacement for the currently running AWS script which allows alexa to interface with my light controller
