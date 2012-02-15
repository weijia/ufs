print "Content-Type: text/html;charset=utf-8"
print ""

import libs.http.queryParam

from Crypto.Cipher import ARC4 as cipher

passwd = 'testpass'

keyobj = cipher.new(passwd)
data = 'data'
d = keyobj.encrypt(data)
print d

passwd = 'testpass'

keyobj = cipher.new(passwd)
data = 'data'
dedata = keyobj.decrypt(d)
print dedata
