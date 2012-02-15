# -*- coding: gb2312 -*- 
import libSys
import libs.localDb.sqliteShove as shove
#import shove
'''
class Defaulting(dict):
...     def __missing__(self, key):
...         self[key] = 'default'
...         return 'default'
'''

class noneEncryptor:
    def __init__(self, encKey = None):
        self.encKey = encKey
    def de(self, encryptedStr):
        return encryptedStr
    def en(self, encryptingStr):
        return encryptingStr
import libs.utils.xorEncryptorUnicode


class nonUnicodeError:
    pass

class simpleEncryptor:
    def __init__(self, encKey):
        self.encKey = encKey
        
    def de(self, encryptedStr):
        if type(encryptedStr) == unicode:
            return libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptedStr)
        raise nonUnicodeError
        
    def en(self, encryptingStr):
        if type(encryptingStr) == unicode:
            return libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptingStr)
        raise nonUnicodeError


        
class simpleEncryptorTxtOut:
    def __init__(self, encKey):
        self.encKey = encKey
        
    def de(self, encryptedStr):
        if type(encryptedStr) == unicode:
            return libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptedStr)
        raise nonUnicodeError
        
    def en(self, encryptingStr):
        if type(encryptingStr) == unicode:
            return libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptingStr)
        raise nonUnicodeError

        
'''
class encryptedShove(dict):
    def __init__(self, storageUrl, encryptor):
        self.dataShove = shove.Shove(storageUrl)
        self.encryptor = encryptor
    def __missing__(self, key):
        self[key] = self.encryptor.de(dataShove[])
        return self[key]
'''
import UserDict
import StringIO
import pickle


class Shove(UserDict.DictMixin):
    '''
    Both key and value should be unicode
    '''
    def __init__(self, storageUrl, encryptor = simpleEncryptorTxtOut):
        self.dataShove = shove.Shove(storageUrl+'.enc', storageUrl+'.enc.cache')
        self.encryptor = encryptor('simpleKey')
    def __getitem__(self, key):
        encryptedKey = self.encryptor.en(key)
        value = self.dataShove[encryptedKey]
        print encryptedKey
        print value
        value = self.encryptor.de(value)
        s = StringIO.StringIO(value.encode('utf8'))
        f = open("d:/testTarget.bin","wb")
        f.write(unicode(s.getvalue()))
        f.close()
        value = pickle.load(s)
        return value

    def __setitem__(self, key, value):
        encryptedKey = self.encryptor.en(key)
        s = StringIO.StringIO()
        pickle.dump(value, s)
        f = open("d:/testSrc.bin","wb")
        f.write(unicode(s.getvalue()))
        f.close()
        print 'load first'
        print unicode(s.getvalue())
        f = open("d:/testSrc.bin","rb")
        t = StringIO.StringIO()
        print pickle.load(f)
        print 'load second'
        f = open("d:/testSrc.bin","rb")
        t = StringIO.StringIO(f.read())
        print pickle.load(t)
        f.close()
        print 'load last'
        t = StringIO.StringIO(s.getvalue())
        print pickle.load(t)
        value = self.encryptor.en(unicode(s.getvalue()))
        print 'final1'
        print value
        newValue = self.encryptor.de(value)
        t = StringIO.StringIO(newValue)
        print pickle.load(t)
        print 'final2'
        print newValue
        print s.getvalue()
        f = open("d:/newValue.bin","wb")
        f.write(newValue)
        f.close()
        f = open("d:/value.bin","wb")
        f.write(value)
        f.close()
        
        print value
        if value == s.getvalue():
            print 'it is the same'
        self.dataShove[encryptedKey] = value
        newValue = self.encryptor.de(self.dataShove[encryptedKey])
        print 'printing new value in dict'
        print newValue
        print 'printing decrypted value'
        print self.encryptor.de(value)
        print 'last compare'
        print self.dataShove[encryptedKey]
        print 'last'
        print value
        
    def __delitem__(self, key):
        encryptedKey = self.encryptor.en(key)
        del self.dataShove[encryptedKey]
    '''
    def keys(self):
        encryptedKeys = self.dataShove.keys()
        res = []
        for i in encryptedKeys:
            res.append(self.encryptor.de(key.decode('utf8')))
            
        return res
    '''
    def keys(self):
        yield self.enumeratorOfKey()
        
    def enumeratorOfKey(self):
        for i in encryptedKeys:
            yield self.encryptor.de(key)

        
if __name__ == "__main__":
    s = Shove("d:/test.enc")
    #s = shove.Shove("sqlite:///d:/test.enc")
    print "你好"
    s[u"你好"] = 1
    print s[u"你好"]