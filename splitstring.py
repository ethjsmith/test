#5/10/19 
def header(selected):

#This is a test function for adding a class to an html element by splitting the strings, and then putting
#them back together. demonstrates the use of the split function
	x="""<div class = "topnav">
	<a href="/">Home</a>
	<a href="/projects">Projects</a>
	<a href="/misc">Misc</a>
	<a href="/blog">Blog</a>
	<a href="/about">About</a>
	<a href="/control">Admin</a>
	</div>
	"""
	if selected == 0:
		return x
	else:
		x = x.split(selected + "\"",1)
		x[0] = x[0] + selected + "\" class = \"current\" "
		z = ' '
		for part in x:
			z+= part
		return z

print header('/projects')
print header(0)
print header('/control')
