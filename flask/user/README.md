required installs : Flask, flask_login, flask_sqlachemy

 currently you can create and load the database like this :
 >>> from vanilla import db
 >>> from vanilla import User
 >>> db.create_all()
 >>> b = User(name='test',password='pass',email='test@b.c')
 >>> db.session.add(b)
 >>> db.session.commit()
 >>> a = User(name='ethan',password='password',email='a')
 >>> db.session.add(a)
 >>> db.session.commit()
 >>> quit()


# ===TODO===
# user management page (personal) (with functionality)
# user management page ( all users (admin)) ( with functionality)
# impliment salting
# moves sensitive information (secret_key) into an external config not saved in github

#deploy

#==QOL==
# WTF forms
# second table for pages


#== Minor ==
# generictemplate.html rework to markup object instead of `|safe` variable ( possible security)
#


stuff from nav 
<a href="/login"{% if request.path == '/login'%} class = 'current'{% endif %} style="float:right;">login</a>
