from Crypto.Cipher import AES
import base64

def correct(msg):
	loop = True
	while (loop == True):
		if (len(msg) % 16 != 0):
			msg = msg + " "
		else:
			loop = False
	return msg

def ejs_encode(msg):
	msg = correct(msg)
	obj = AES.new('This is a key123', AES.MODE_CBC,'2348123444554455')
	coded = obj.encrypt(msg)
	return coded

def ejs_decode(msg):
	objj = AES.new('This is a key123',AES.MODE_CBC,'2348123444554455')
	plaintxt = objj.decrypt(msg)
	return plaintxt

pre16 = raw_input('encrypt a thing: ')
test2 = ejs_encode(pre16)
print base64.b64encode(test2)
test3 = ejs_decode(test2)
print test3
