chars = []
something = [0x70,0x61,0x73,0x73,0x77,0x6f,0x72,0x64,0x21,0x21]
something2 = [0x74,0x68,0x69,0x73,0x20,0x69,0x73,0x20,0x61,0x20,0x74,0x72,0x6f,0x6c,0x6c]

for s in something:
	chars.append(chr(5 ^ s))
z = "".join(chars)
print z
for s in something2:
	chars.append(chr(s + 0xA))
s = "".join(chars)
print s
