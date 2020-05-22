WEB app for keeping track of spell cooldowns during combat (and maybe more) )

TODO:
* user authentication to access the site
* ~~Character abilities / equipment usage~~
* ~~UI improvements~~
* testing testing testing
* ~~fix for when pressing enter on unfilled tables~~
* ~~buttons for taking long rest, and recharging items~~
* DNS name for site :^)
* Fix gitignore
* fix casting other player's spells
* 
*


Script for creating test database from scratch
```
from app import Character,Spell,db
db.create_all()
a=Character("Azog","Wizard")
b=Character("Doug","Cleric")
c=Spell("fireball",3,1)
d=Spell("Magic Missle",2,1)
e = Spell("heal",2,2)
f = Spell("Great Heal", 3,2)
db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.add(d)
db.session.add(e)
db.session.add(f)
db.session.commit()
```
