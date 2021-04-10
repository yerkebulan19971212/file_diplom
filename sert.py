import base64
s = "Hello World!"
b = s.encode("UTF-8")
e = base64.b64encode(b)
s1 = e.decode("UTF-8")
print("Base64 Encoded:", s1)
s1 = 'JVBERi0xLjYNJeLjz9MNCjM3IDAgb2JqIDw8L0xpbmVhcml6ZWQgMS9MIDIwNTk3L08gNDAvRSAx'
b1 = s1.encode("UTF-8")
d = base64.b64decode(b1)
print(d)
s2 = d.decode("ascii")
print(s2)