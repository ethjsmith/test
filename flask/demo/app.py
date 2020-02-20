from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == 'POST':
        return """
        <html>
            <body>
                Welcome, """ + request.form['uname'] + """
            </body>
        </html>"""
    else:
        return """
            </html>
                </body>
                    Hello, please enter your name !
                    or ... try inserting something weird into the box and see what happens!
                    <form method = "POST" enctype = "multipart/form-data">
                        <input type='text' name =uname></input>
                        <input type = "submit" value = "submit"/>
                    </form>
                </body>
            </html>"""





if (__name__ == "__main__"):
    app.run()
