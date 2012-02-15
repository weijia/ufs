
from google.appengine.ext import db
from libs.ufsDb.ufsDbBase import *
currentGaeEntryDbVersion = 1

class ufsEntry(db.Model):
  #user id for this entry
  owner = db.StringProperty(required=True)
  #database id for this entry
  dbId = db.StringProperty(required=True)
  objId = db.StringProperty(required=True)
  #entry key id
  keyId = db.StringProperty(required=True)
  valueId = db.StringProperty(required=True)
  #The following is used to enable query an key value mapping in one field, it must be consistent with the above 2 fields
  keyIdValueIdMapping = db.StringProperty(required=True)
  
  modifiedDate = db.DateTimeProperty(auto_now_add=True)
  createApp = db.StringProperty()
  #Transaction id, will be set to 0 if the transaction is commited. Otherwise, it contain the transaction id
  #Update and remove can not use this mechanism, so remove this.
  #transId = db.IntegerProperty()
  #partition id, used to partition the data so the query result will always less than 1000. Reserved currently
  partitionId = db.IntegerProperty()
  #The entry db version
  version = db.IntegerProperty()
  


class ufsDbGaeEntryDb(ufsDbEntryDbInterface):
  def __init__(self, entryDbOwer, entryDbId):
    self.entryDbOwer = entryDbOwer
    self.entryDbId = entryDbId
  def add(self, objId, k, v, createapp):
    #Check if the record is already there
    q = db.GqlQuery("SELECT * FROM ufsEntry " +
                "WHERE objId = :1 AND owner = :2 AND dbId = :3 AND keyId = :4 AND valueId = :5 " +
                "ORDER BY __key__",
                objId, self.entryDbOwer, self.entryDbId, k, v)
    results = q.fetch(1)
    for p in results:
      return
    #Add the record
    e = ufsEntry(owner = self.entryDbOwer,
          dbId = self.entryDbId,
          objId = objId,
          keyId = k,
          valueId = v,
          keyIdValueIdMapping = k+'='+v,
          createApp = createapp,
          version = currentGaeEntryDbVersion
        )
    e.put()

  def update(self, objId, k, v, nv):
    q = db.GqlQuery("SELECT * FROM ufsEntry " +
                "WHERE objId = :1 AND owner = :2 AND dbId = :3 AND keyId = :4 AND valueId = :5 " +
                "ORDER BY __key__",
                objId, self.entryDbOwer, self.entryDbId, k, v)
    if q.count() > 1:
      raise 'multipile ufsEntry exists'
    results = q.fetch(5)
    for p in results:
      p.valueId = nv
      p.keyIdValueIdMapping = k+'='+nv
      p.put()
      return
    #Do not exist
    raise 'no existing value'
  def getAttr(self, objId, k):
    '''
    q = db.GqlQuery("SELECT * FROM ufsEntry " +
                "WHERE objId = :1 AND owner = :2 AND dbId = :3 AND keyId = :4 " +
                "ORDER BY __key__",
                objId, self.entryDbOwer, self.entryDbId, k)
    '''
    q = db.GqlQuery("SELECT * FROM ufsEntry " +
                "WHERE objId = :1 AND owner = :2 AND dbId = :3 AND keyId = :4 " +
                "ORDER BY __key__",
                objId, self.entryDbOwer, self.entryDbId, k)
    results = q.fetch(5)
    print 'query:', objId, ',', k,',',self.entryDbOwer,',', self.entryDbId,',',results
    cnt = 0
    for p in results:
      print 'item:%d, %s'%(cnt,p.valueId)
      cnt += 1
      return p.valueId
  def hasKey(self, keyId):
    pass
  def runInTransaction(self, f):
    pass
  def getObjIdListAllCondition(self, keyValueIdPair, offset = 0, limit = 20):
    #Find the key value pair with least returned data.
    pass
  def getObjIdListOneCondition(self, keyValueIdPair, offset = 0, limit = 20):
    pass
