#! /bin/python3

# Testing how to open files and pass variables from one file to another 

import getpass

pw = getpass.getpass("")

with open("stolen.txt", 'w') as f:
	if len(pw) > 0:
		f.write(pw)

print (pw)

