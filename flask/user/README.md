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
# user management page (personal)
# user management page ( all users (admin))
# topbar change that adds your usename/login status
# impliment salting
# moves sensitive information (like secret key and hash/salt info into an external config not saved in github)

#deploy

#==QOL==
# WTF forms
# second table for pages
# wait, what's happening here!
# this might end up being a real website
