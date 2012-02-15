import ufsDbBase

from Crypto.Cipher import ARC4 as cipher



class encryptionManager:
  def __init__(self, k):
    #self.session = session
    self.k = k
  def encrypt(self, data):
    #k = session.getValue('userMasterPassword')
    keyobj = cipher.new(self.k)
    return keyobj.encrypt(data)
  def decrypt(self, data):
    #k = session.getValue('userMasterPassword')
    keyobj = cipher.new(self.k)
    return keyobj.decrypt(data)


class ufsDbEncryptedTokenDb(ufsDbBase.ufsDbTokenDbInterface):
  def __init__(self, tokenDb, cyptoMgr):
    self.tokenDb = tokenDb
    self.cyptoMgr = cyptoMgr
  def get(self, tokenId):
    token = self.tokenDb.get(tokenId)
    return self.cyptoMgr.decrypt(token)
  def getId(self, token):
    encryptedToken = self.cyptoMgr.encrypt(token)
    return self.tokenDb.getId(encryptedToken)
