from Crypto.Cipher import ARC4 as cipher
import md5
import random
import base64

class encryptionManager:
  def __init__(self, user, keyDbId):
    self.user = user
    self.keyDbId = keyDbId
  def encrypt(self, value, key):
    keyobj = cipher.new(key)
    return base64.b64encode(keyobj.encrypt(value))
  
  def decryption(self, value, key):
    keyobj = cipher.new(key)
    return keyobj.decrypt(base64.b64decode(value))
    
  def getRandomKey(self):
    return str(md5.new(str(random.random())).hexdigest())