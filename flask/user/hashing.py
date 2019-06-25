# to be used with python3
import hashlib

password = "yellow"

h = hashlib.md5(password.encode())
#print h

pass2 = "password"

pass3 = "something"

h2 = hashlib.md5(pass2.encode())
h3 = hashlib.md5(pass3.encode())


#compares 2 hashed objects
def compare(h1,h2):
    #print(h1.digest())
    #print(h2.digest())
    if h1.digest() == h2.digest():
        return True
    return False

#print(compare (h,h2))
#print(compare (h2,h3))
#print(compare(h2,h))
pas = input("enter your password: ")
usr = hashlib.md5(pas.encode())
if compare(usr,h):
    print ("Success")
else:
    print ("failed")
