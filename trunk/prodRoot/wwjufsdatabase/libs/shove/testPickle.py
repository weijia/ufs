# -*- coding: gb2312 -*- 
import pickle
#f = open('d:/testSrc.bin','rb')
import libSys
from encryptedShoveV3 import *
encryptor = simpleEncryptor('simpleKey')
#print encryptor.de(unicode(f.read()))
uv = u"你好"
import StringIO
s = StringIO.StringIO()
pickle.dump(uv, s)
print '----------------testing pickle'
f = open("d:/tmp.bin", "wb")
f.write(unicode(s.getvalue()))
f.close()
f = open("d:/tmp.bin", "rb")

s = StringIO.StringIO(f.read())
print pickle.load(s)
f.close()
print '----------------testing encryptor'
v = encryptor.en(u"你好")

encryptor.de(v)

print '----------------testing dict'
import libs.localDb.sqliteShove as shove
dataShove = shove.Shove('testSqliteShove','hi')

f = open('d:/testSrc.bin','rb')
v = f.read()
dataShove["good"] = v
f.close()
print '--------------'
print dataShove["good"]
print '--------------'
print v
#v = pickle.load(f)
