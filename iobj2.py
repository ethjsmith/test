import iterateobject
funcs = []
obj = iterateobject.obj()
#I've heard rumors that this is bad codiing practice... oh well
for z in dir(obj):
	if not z.startswith("__"):
		if callable(getattr(obj,z)):
			callme = getattr(obj,z)
			print callme()
#print dir(obj)
