# -*- coding: utf-8 -*- 
import libSys
#import libs.localDb.sqliteShove as shove
import shove
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
    def __init__(self, storageUrl, encryptor = simpleEncryptor):
        self.dataShove = shove.Shove(storageUrl+'.enc', storageUrl+'.enc.cache')
        self.encryptor = encryptor('simpleKey')
    def __getitem__(self, key):
        encryptedKey = self.encryptor.en(key.decode('utf8'))
        value = self.dataShove[encryptedKey]
        value = self.encryptor.de(value).encode('utf8')
        s = StringIO.StringIO(value)
        value = pickle.load(s)
        return value

    def __setitem__(self, key, value):
        encryptedKey = self.encryptor.en(key.decode('utf8'))
        s = StringIO.StringIO()
        pickle.dump(value, s)
        value = self.encryptor.en(unicode(s.getvalue()))
        self.dataShove[encryptedKey] = value
        
    def __delitem__(self, key):
        encryptedKey = self.encryptor.en(key.decode('utf8'))
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
            yield self.encryptor.de(key.decode('utf8'))

        
if __name__ == "__main__":
    s = Shove("sqlite:///d:/test.enc")
    #s = shove.Shove("sqlite:///d:/test.enc")
    print "你好"
    s["你好".decode('utf8')] = "你好啊".decode('utf8')
    #print s["你好".decode('gb2312')]