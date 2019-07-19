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


== Minor ==
. generictemplate.html rework to markup object instead of `|safe` variable ( possible security)


admin functionality
.add articles
.delete files (?)
.manage Users

currently you can create and load the database like this :
```python
from vanilla import db
from vanilla import User,Post
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
quit()
```
<p> School is filled with requirements to do lots of things, so on this page I'll write about some of the cooler, or more interesting things that I think I've done to complete various assignments</p>
		<p>I've used github for a long time, so most of my projects are up there, and I can link them as well, so that's pretty nice.</p>
		<p> The first time I really felt like I went above and beyond was for my BYUI CS101 class. The professor 'taught' us python, by basically having us follow the Code Academy course, and then had us do a 'final project' of our choosing. Me and my cousin Jared Wrathall ( who was a senior at the time, and probably did most of the heavy lifting) made a simple text adventure game, where you move around a map made of X's, looking for enemies, and gaining loot, through randomized, pokemon style text based encounters. I felt pretty good about the project, until I looked at what other people were doing, and realized that we could have just made a basic calculator or something, but either way, it was fun to make, and I enjoyed going all out for a project, and that attitude has stuck with me for all my programming classes.
		You can check out the source code <a href = 'https://github.com/ddrgrevious/textadventure'> Right here </a></p>
		<p> The second 'big for it's time' project I did was in my BYUI CIT-160 javascript programming class. Our teacher showed us how to draw in a screen, and I realized that I could update that screen, by redrawing the screen (and discovering basic animation), and so I decided to use this technique to recreate the classic 'Pong' game in javascript.
		It was really interesting for me, because it taught me a lot about game design, ( like how a game loop works, and variable scope), as well as how useful functions really are. and as a bonus the class was really impressed, because it was a very simple class, and most of the rest of the projects weren't even graphical in nature. I have that source code ( or most of it anyways) up on my github <a href='https://github.com/urd000med/urd000med_pong'> Right here </a></p>
		<p> I wasn't really engaged in my first programming class at SUU, which I didn't think I should have even been in, but was anyway, because my adviser disagreed with me ( she was and still is wrong ), so when it was suggested that we would be working on a giant final project for half the semester I decided that I was going to make something crazy. This class had a similar scope to my last one, with nothing crazy going on , and so I decided to follow pong, with Asteroids. This ended up being quite a large commitment of time, and energy, as it was the largest project I had ever undertaken, and there was lots of objects working with each other, plus it was written in java, a language that, until that semester, I had no experience with.
		The project ended up turning out pretty good, with the basic mechanics working fine, although there is more that I would have wanted to add, if I had more time, and energy, (like the asteroids splitting into smaller asteroids when hit, or a prettier loading screen ) <a href = 'https://github.com/urd000med/1400final'> You can view the java code here </a></p><br>
		<p> In my 1410 class I ended up making a pretty standard final tower defence project (which is in a private github repo, so no code for now, sorry ) but I did go above and beyond in adding a lot of cool quality of life improvements, like when you kill an enemy it's corpse stays on the screen for awhile, and animated enemy movement. This was one of the first sometimes
		that I really understood how complicated making crazy advanced games is, because I had to draw all the sprites myself, and I kept running into problems which I should have fixed in a parent class, but instead I tried to patch quickly in a child. I also saw how much math really can go into a complicated project. I tried to make a tower that shot lightning , by picking a random point about halfway between the target enemy,
		and the firing tower. but to do that you need to use some complicated trigonometry. it was a really interesting, and eye opening experience trying to change numbers slightly to get the desired effect, and wishing I understood math a bit better.</p>
		<p> Hopefully I'll have some more crazy projects to write about here later, but until then, this is is!</p>
