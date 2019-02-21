import os
import platform
import getpass

user =  getpass.getuser()
sys =  platform.system()

if (sys == "Windows):
	#do stuff
else if (sys == "Linux"):
	#check for root
else:
	#do stuff
