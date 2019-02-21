testval = 'this is test'
loop = True
print len(testval)
while (loop == True):
	if (len(testval) % 15 != 0):
		testval = testval + ' '
	else:
		loop = False

print len(testval)
