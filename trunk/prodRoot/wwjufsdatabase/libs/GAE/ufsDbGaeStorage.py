import libs.ufsDb.ufsDbBaseInterface
from google.appengine.ext import db

currentGaeStorageVersion = 1

import sys

class ufsStorage(db.Model):
  #user id for this entry
  owner = db.StringProperty(required=True)
  #database id for this entry
  dbId = db.StringProperty(required=True)
  objId = db.StringProperty(required=True)
  #entry key id
  data = db.BlobProperty()
  modifiedDate = db.DateTimeProperty(auto_now=True)
  createdDate = db.DateTimeProperty(auto_now_add=True)
  createApp = db.StringProperty()
  #The token db version
  version = db.IntegerProperty()
  valid = db.BooleanProperty(required=True)

class ufsDbGaeStorage(libs.ufsDb.ufsDbBaseInterface.ufsDbTextStorageInterface):
  def __init__(self, owner, dbId):
    self.owner = owner
    self.dbId = dbId
  def storeData(self, key, data, createapp = sys.argv[0]):
    '''
    data: must be string object. Can use str.encode('utf-8') to encode unicode to string
    '''
    q = db.GqlQuery("SELECT * FROM ufsStorage " +
                "WHERE owner = :1 AND dbId = :2 AND objId = :3 AND valid = :4 " +
                "ORDER BY __key__",
                self.owner, self.dbId, key, True)
    result = q.fetch(1)
    for i in result:
      i.valid = False
      i.put()
    o = ufsStorage(
      owner = self.owner,
      dbId = self.dbId,
      objId = key,
      data = data,
      createApp = createapp,
      version = currentGaeStorageVersion,
      valid = True
    )
    o.put()

  def getData(self, key):
    q = db.GqlQuery("SELECT * FROM ufsStorage " +
                "WHERE owner = :1 AND dbId = :2 AND objId = :3 AND valid = :4 " +
                "ORDER BY __key__",
                self.owner, self.dbId, key, True)
    result = q.fetch(1)
    for i in result:
      #print 'got data:',i.data
      return i.data
      
    #print 'no data',self.owner, self.dbId, key
    return None
      
import libs.ufsDb.ufsDbBaseInterface
import uuid

class ufsDbGaeStorageTokenDb(libs.ufsDb.ufsDbBaseInterface.ufsDbTokenDbInterface):
  def __init__(self, owner, dbId):
    self.storage = ufsDbGaeStorage(owner, dbId)
  def getId(self, token):
    id = str(uuid.uuid4())
    self.storage.storeData(id, token)
    return id
    
  def get(self, tokenId):
    #print 'get storage:',tokenId
    return self.storage.getData(tokenId)
