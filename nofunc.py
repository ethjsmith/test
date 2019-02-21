class oop:
	def test1(self):
		return True
	def test0(self):
		return "it works I think"
	def test2(self):
		return "something"
#	def test4(name):
#		return getattr(self,name,test2)
	def test3(var):
		try:
			# call a dynamicfunction >
			exists = var()
			return exists 
		except:
			# do something else
			return "didn't work"

#try:
#	testtt()
#except:
#	print "doesn't exist dummy"
	#print test4('test0')
if __name__ == "__main__":
	obj = oop()
#	print obj.test4()
	z =  getattr(obj,"tezzst0","test2")
	print z()
