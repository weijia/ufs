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

class binHex:
    def en(self, s):
        res = ''
        for i in s:
            res += "%02X"%ord(i)
        #print res
        return res
    def de(self, s):
        res = ''
        flag = False
        left = ''
        for i in s:
            if flag:
                left +=i
                res += chr(int(left, 16))
                flag = False
            else:
                left = i
                flag = True
        #print res
        return res
        
        
class simpleEncryptorTxtOut:
    def __init__(self, encKey):
        self.encKey = encKey
        self.binHex = binHex()
        
    def de(self, encryptedStr):
        if type(encryptedStr) == unicode:            
            return libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(self.binHex.de(encryptedStr))
        raise nonUnicodeError
        
    def en(self, encryptingStr):
        if type(encryptingStr) == unicode:
            return self.binHex.en(libs.utils.xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptingStr))
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
        key = unicode(key)
        encryptedKey = self.encryptor.en(key)
        value = self.dataShove[encryptedKey]
        if False:
            f = open("d:/testTarget.bin","wb")
            f.write(value)
            f.close()
        #print '-------------------------'
        #print value
        value = self.encryptor.de(value)
        #print '-------------------------'
        #print value
        s = StringIO.StringIO(value.encode('gb2312'))
        #s = StringIO.StringIO(value)
        if False:
            f = open("d:/testTarget.bin","wb")
            f.write(unicode(s.getvalue()))
            f.close()
        value = pickle.load(s)
        return value

    def __setitem__(self, key, value):
        key = unicode(key)
        encryptedKey = self.encryptor.en(key)
        s = StringIO.StringIO()
        pickle.dump(value, s)
        if False:
            f = open("d:/testSrc.bin","wb")
            f.write(unicode(s.getvalue()))
            f.close()
        
        value = self.encryptor.en(unicode(s.getvalue()))
        if False:
            f = open("d:/testSrc.bin","wb")
            f.write(value)
            f.close()
        
        self.dataShove[encryptedKey] = value
        #print value
        
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
    #s[u"你好"] = u"你好啊"
    #print s[u"你好"]
    s[u"hello"] = u"201012051538goodbye"
    print s[u"hello"]
    s[u"good"] = [u"你好",u"再见"]
    for i in s[u"good"]:
        print i