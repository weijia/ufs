# -*- coding: utf-8 -*- 
import libSys
import libs.localDb.sqliteShove as shove
#import shove
import UserDict
import StringIO
import pickle


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

import binhex
        
class simpleEncryptorTxtOut:
    def __init__(self, encKey):
        self.encKey = encKey
        
    def de(self, encryptedStr):
        if type(encryptedStr) == unicode:
            s = StringIO.StringIO(encryptedStr)
            t = StringIO.StringIO(u"")
            binhex.hexbin(s, t)
            return libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(t)
        raise nonUnicodeError
        
    def en(self, encryptingStr):
        if type(encryptingStr) == unicode:
            s = StringIO.StringIO(encryptingStr)
            t = StringIO.StringIO(u"")
            binhex.binhex(s, t)
            return base64.b64encode(libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(t))
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
        value = self.encryptor.de(value)
        s = StringIO.StringIO(value)
        f = open("d:/testTarget.bin","wb")
        f.write(s.getvalue())
        f.close()
        value = pickle.load(s)
        return value

    def __setitem__(self, key, value):
        encryptedKey = self.encryptor.en(key)
        s = StringIO.StringIO()
        pickle.dump(value, s)
        f = open("d:/testSrc.bin","wb")
        f.write(s.getvalue())
        f.close()
        value = self.encryptor.en(unicode(s.getvalue()))
        self.dataShove[encryptedKey] = value
        
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
    s["你好".decode('gb2312')] = "你好啊".decode('gb2312')
    print s["你好".decode('gb2312')]