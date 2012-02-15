from google.appengine.ext import db
from libs.ufsDb.ufsDbBaseInterface import *

currentGaeTokenDbVersion = 1

class ufsToken(db.Model):
  #user id for this entry
  owner = db.StringProperty(required=True)
  #database id for this entry
  dbId = db.StringProperty(required=True)
  strValue = db.StringProperty()
  intValue = db.IntegerProperty()
  #blobValue = db.BlobProperty()
  #type = 1, the token is a string
  #type = 2, the token is an int
  type = db.IntegerProperty(required=True)
  #KeyHandle for the token, to reduce the complexity, token db uses a same key so the entry db will get only 1
  #token ID for 1 token.
  #keyHandle = db.StringProperty()
  #The token db version
  version = db.IntegerProperty()

class ufsDbGaeTokenNotExist:
  pass
  

class ufsDbGaeTokenDb(ufsDbTokenDbInterface):
  def __init__(self, owner, dbId):
    if owner is None:
        raise 'owner can not be None'
    if dbId is None:
        raise 'dbId can not be None'
    self.owner = owner
    self.dbId = dbId
  def get(self, tokenId):
    q = self.getTokenFromId(tokenId)
    if q is None:
      raise ufsDbGaeTokenNotExist
    return q.strValue
  def getTokenFromId(self, tokenId):
    #print tokenId
    return ufsToken.get(tokenId)
  def getIdFromToken(self, token):
    q = db.GqlQuery("SELECT * FROM ufsToken " +
                "WHERE owner = :1 AND dbId = :2 AND strValue = :3 " +
                "ORDER BY __key__",
                self.owner, self.dbId, token)
    result = q.fetch(1)
    for i in result:
      return i
    return None
    
  def getId(self, token):
    q = self.getIdFromToken(token)
    if q is None:
      q = ufsToken(
        owner = self.owner,
        dbId = self.dbId,
        strValue = token,
        #type = 1, the token is a string
        #type = 2, the token is an int
        type = 1,
        version = currentGaeTokenDbVersion
      )
      q.put()
    return str(q.key())