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
import libs.utils.xorEncryptor

class simpleEncryptor:
    def __init__(self, encKey):
        self.encKey = encKey
        
    def de(self, encryptedStr):
        return libs.utils.xorEncryptor.PEcrypt(self.encKey).Crypt(encryptedStr)
        
    def en(self, encryptingStr):
        return libs.utils.xorEncryptor.PEcrypt(self.encKey).Crypt(encryptingStr)
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
        self.dataShove = shove.Shove(storageUrl+'.enc')
        self.encryptor = encryptor('simpleKey')
    def __getitem__(self, key):
        encryptedKey = self.encryptor.en(key)
        value = self.dataShove[encryptedKey]
        value = self.encryptor.de(value)
        s = StringIO.StringIO(value)
        value = pickle.load(s)
        return value

    def __setitem__(self, key, value):
        encryptedKey = self.encryptor.en(key)
        s = StringIO.StringIO()
        pickle.dump(value, s)
        value = self.encryptor.en(s.getvalue())
        self.dataShove[encryptedKey] = value
        
    def __delitem__(self, key):
        encryptedKey = self.encryptor.en(key)
        del self.dataShove[encryptedKey]
        
    def keys(self):
        pass
        