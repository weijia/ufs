from Crypto.Cipher import ARC4 as cipher
import md5
import random
import base64

class nonUnicode: pass

class arc4EncryptorOld:
  def __init__(self, user = None, keyDbId = None):
    self.user = user
    self.keyDbId = keyDbId
  def en(self, value, key):
    if type(value) != unicode:
        raise nonUnicode
    keyobj = cipher.new(key)
    return base64.b64encode(keyobj.encrypt(value.encode('utf8')))
  
  def de(self, value, key):
    v = base64.b64decode(value)
    keyobj = cipher.new(key)
    return keyobj.decrypt(v).decode('utf8')
    
  def getRandomKey(self):
    return str(md5.new(str(random.random())).hexdigest())
    
class arc4Encryptor:
    def __init__(self, encKey):
        '''
        All strings should be unicode
        '''
        self.encKey = encKey
    def en(self, value):
        if type(value) != unicode:
            raise nonUnicode
        keyobj = cipher.new(self.encKey)
        return keyobj.encrypt(value.encode('utf8'))

    def de(self, value):
        keyobj = cipher.new(self.encKey)
        return keyobj.decrypt(value).decode('utf8')
    
class encryptorBase64Out:
    def __init__(self, encKey, encryptor = arc4Encryptor):
        '''
        All strings should be unicode
        '''
        self.encryptor = encryptor(encKey)
    def en(self, value):
        if type(value) != unicode:
            raise nonUnicode
        return unicode(base64.b64encode(self.encryptor.en(value)))

    def de(self, value):
        if type(value) != unicode:
            raise nonUnicode
        v = base64.b64decode(value)
        return self.encryptor.de(v)
    


'''
#Does not work
class encryptor:
  def __init__(self, user = None, keyDbId = None):
    self.user = user
    self.keyDbId = keyDbId
  def en(self, value, key):
    if type(value) != unicode:
        raise nonUnicode
    keyobj = cipher.new(key)
    return keyobj.encrypt(value.encode('utf8'))
  
  def de(self, value, key):
    #v = base64.b64decode(value)
    keyobj = cipher.new(key)
    return keyobj.decrypt(value).decode('utf8')
    
  def getRandomKey(self):
    return str(md5.new(str(random.random())).hexdigest())
'''