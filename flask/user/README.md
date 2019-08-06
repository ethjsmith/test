Flask user : a dynamic flask site with users, and a database to store both users and articles. (this is basically the staging/building area for a huge upgrade to rpi_lightserver)

(must be python3)
run `python vanilla.py`

required installs : Flask, flask_login, flask_sqlachemy

 ===TODO===
. user management page (personal) (with functionality)
. allow creation of pages from admin page (?or elsewhere?)
. moves sensitive information (secret_key) into an  external config not saved in GitHub

# deploy

==QOL==
. WTF forms
. second table for pages
. db link between articles(/content) and users

== Minor ==
. generictemplate.html rework to markup object instead of `|safe` variable ( possible security)


admin functionality
.add articles
.delete files (?)
.manage Users

currently you can create and load the database like this :
```python
from vanilla import db
from vanilla import User,Post,Comment
db.create_all()
#two example users
b = User(name='test',password='pass',email='test@b.c')
a = User(name='ethan',password='password',email='a')
# add and save the users
db.session.add(b)
db.session.add(a)
db.session.commit()
#example of an article
p1 = Post(topic="misc",title="Example Article",picture="/static/Pic.jpg",body="This is the body of the article, which accepts <i> HTML tags </i>")
db.session.add(p1)
db.session.commit()
c = Comment(title='test',message='I love testing',poster=1,article=1)
db.session.add(c)
db.session.commit()
quit()
```
