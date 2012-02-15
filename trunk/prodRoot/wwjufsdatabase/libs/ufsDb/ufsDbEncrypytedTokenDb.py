import ufsDbBase


class ufsDbEncryptedTokenDb(ufsDbTokenDbInterface):
  def __init__(self, tokenDb, keyManager):
    self.tokenDb = tokenDb
    self.keyManager = keyManager
  def get(self, tokenId):
    token = self.tokenDb.get(tokenId)
    return self.keyManager.decrypt(token)
  def getId(self, token):
    encryptedToken = self.keyManager.encrypt(token)
    return self.tokenDb.getId(encryptedToken)
