from google.appengine.ext import db
from libs.ufsDb.ufsDbBase import *
currentGaeEntryDbVersion = 1

class ufsEntry(db.Expando):
  #user id for this entry
  owner = db.StringProperty(required=True)
  #database id for this entry
  dbId = db.StringProperty(required=True)
  objId = db.StringProperty(required=True)
  #entry key id
  keyId = db.StringProperty(required=True)
  valueId = db.StringProperty(required=True)
  modifiedDate = db.DateTimeProperty(auto_now=True)
  createdDate = db.DateTimeProperty(auto_now_add=True)
  createApp = db.StringProperty()
  #The entry db version
  version = db.IntegerProperty()
  valid = db.BooleanProperty(required=True)
  

class ufsDbGaeEntryDb(ufsDbEntryDbInterface):
  def __init__(self, entryDbOwer, entryDbId):
    self.entryDbOwer = entryDbOwer
    self.entryDbId = entryDbId
  def genAttrPair(self, k, v):
    return k+'_'+v
  def add(self, objId, k, v, createapp):
    #Check if the record is already there
    q = ufsEntry.all()
    q.filter("objId =", objId)#All filter should has space before '=', 'objId=' will not work
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter(self.genAttrPair(k,v)+'=', True)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(1)
    for p in results:
      return
    #The object does not exist in the database.
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')


    results = q.fetch(1)
    newAttr = {}
    for p in results:
      #Obj exists, add attribute
      self.getDynamicAttr(p)
      
      #Add the new attribute
      newAttr[self.genAttrPair(k,v)] = True
      #print newAttr
      u = ufsEntry(
        owner = p.owner,
        dbId = p.dbId,
        objId = p.objId,
        keyId = p.keyId,
        valueId = p.valueId,
        createdDate = p.createdDate,
        createApp = p.createApp,
        version = p.version,
        valid = p.valid,
        **newAttr)
      p.valid = False
      p.put()
      u.put()
      return
    #Object not exists
    newAttr = {self.genAttrPair(k,v): True}
    u = ufsEntry(
      owner = self.entryDbOwer,
      dbId = self.entryDbId,
      objId = objId,
      keyId = k,
      valueId = v,
      createApp = createapp,
      version = currentGaeEntryDbVersion,
      valid = True,
      **newAttr)
    u.put()
    
  
  def getDynamicAttr(self, obj):
    l = obj.dynamic_properties()
    newAttr = {}
    for i in l:
      newAttr[i] = getattr(obj, i)
    return newAttr
  
  #Update can be replaced by delete attrbute and add new attribute
  def update(self, objId, k, v, nv, createapp):
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter(self.genAttrPair(k,v)+'=', True)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(1)
    for p in results:
      n = self.getDynamicAttr(p)
      n[self.genAttrPair(k,nv)] = True
      n[k] = True
      u = ufsEntry(
        owner = p.owner,
        dbId = p.dbId,
        objId = p.objId,
        createdDate = p.createdDate,
        createApp = p.createApp,
        version = currentGaeEntryDbVersion,
        **n)
      p.valid = False
      p.put()
      u.put()
      return
  
  def getValueIdFromPair(self, keyValuePair):
    print 'getting key value paire from:',keyValuePair
    return keyValuePair.split('_')[1]
  
  def getAttr(self, objId, k):
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter('keyId =', k)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(1)
    for p in results:
      return p.valueId
    #print 'no attribute got'
    return None
  def hasKey(self, keyId):
    pass
  def runInTransaction(self, f):
    pass
  def getObjIdListAllCondition(self, keyValueIdPair, offset = 0, limit = 20):
    q = ufsEntry.all()
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    for k in keyValueIdPair.keys():
      q.filter(self.genAttrPair(k,keyValueIdPair[v])+'=', True)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(limit, offset)
    res = []
    for p in results:
      res.append(p.objId)
    return res

  def getObjIdListOneCondition(self, keyValueIdPair, offset = 0, limit = 20):
    of = offset
    li = 0
    res = []
    for k in keyValueIdPair.keys():
      q = ufsEntry.all()
      q.filter("owner =", self.entryDbOwer)
      q.filter("dbId =", self.entryDbId)
      q.filter("valid =", True)

      q.filter(self.genAttrPair(k,keyValueIdPair[v])+'=', True)
      #q.order("__key__")
      q.order('modifiedDate')
      l = q.fetch(limit-li, of)
      if len(results) == 0:
        #No result at of(fset) position.
        of = of - q.count()
        continue
      
      for p in results:
        res.append(p.objId)
        cnt += 1
        if cnt >= limit:
          return res


class ufsSimpleDbGaeEntryDb(ufsSimpleDbEntryDbInterface):
  def __init__(self, entryDbOwer, entryDbId):
    self.entryDbOwer = entryDbOwer
    self.entryDbId = entryDbId

  def getObjIdList(self, keyId, valueId, offset = 0, limit = 20):
    q = ufsEntry.all()
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)#All filter should has space before '=', 'dbId=' will not work
    q.filter("keyId =", keyId)
    q.filter("valueId =", valueId)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(limit, offset)
    #print 'in getObjIdList:',results
    #print self.entryDbId,self.entryDbOwer,offset,limit,keyId, valueId
    res = []
    for i in results:
      res.append(i.objId)
    return res
  def getAttr(self, objId, k):
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter('keyId =', k)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(1)
    for p in results:
      return p.valueId
    #print 'no attribute got'
    return None
  def getOffsetTimeStamp(self, objId, k, offset):
    if offset < 1000:
      q = ufsEntry.all()
      q.filter("objId =", objId)
      q.filter("owner =", self.entryDbOwer)
      q.filter("dbId =", self.entryDbId)
      q.filter('keyId =', k)
      q.filter("valid =", True)
      #q.order("__key__")
      q.order('-modifiedDate')
      results = q.fetch(1, offset)
      for p in results:
        return p.modifiedDate
      #raise "no item at offset:%d"%offset
      return None
    else:
      #Start point larger than 1000
      raise "not supported yet:%d"%offset
      q = ufsEntry.all()
      q.filter("objId =", objId)
      q.filter("owner =", self.entryDbOwer)
      q.filter("dbId =", self.entryDbId)
      q.filter('keyId =', k)
      q.filter("valid =", True)
      #q.order("__key__")
      q.order('-modifiedDate')
      results = q.fetch(limit, offset)
      res = []
      for p in results:
        res.append(p.valueId)
      return res
    
    
  def getAttrList(self, objId, k, offset = 0, limit = 20):
    firstOffset = self.getOffsetTimeStamp(objId, k, offset)
    if firstOffset is None:
      #raise "No item offset:%d, limit:%d"%(offset, limit)
      return []
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter('keyId =', k)
    q.filter("valid =", True)
    q.filter("modifiedDate <= ",firstOffset)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(limit, offset)
    res = []
    for p in results:
      res.append(p.valueId)
    return res

  def add(self, objId, keyId, valueId, createapp):
    #Check if the record is already there
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter("keyId =", keyId)
    q.filter("valueId =", valueId)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(1)
    for p in results:
      return
    #Object not exists
    u = ufsEntry(
      owner = self.entryDbOwer,
      dbId = self.entryDbId,
      objId = objId,
      keyId = keyId,
      valueId = valueId,
      createApp = createapp,
      version = currentGaeEntryDbVersion,
      valid = True)
    u.put()

  def update(self, objId, keyId, valueId, newValue, createapp):
    #print 'ufsDbGaeEntryDb:',keyId, valueId
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter("keyId =", keyId)
    q.filter("valueId =", valueId)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(10)
    #print keyId, valueId
    '''
    for p in results:
      # u = ufsEntry(
        # owner = p.owner,
        # dbId = p.dbId,
        # objId = p.objId,
        # keyId = p.keyId,
        # valueId = p.valueId,
        # createdDate = p.createdDate,
        # createApp = p.createApp,
        # version = currentGaeEntryDbVersion)
      p.keyId = keyId
      p.valueId = valueId
      p.put()
      return
    '''
    for p in results:
      #print p.objId
      p.valid = False
      p.put()
    self.add(objId, keyId, newValue, createapp)
  def delete(self, objId, keyId, valueId):
    #print 'ufsDbGaeEntryDb:',keyId, valueId
    q = ufsEntry.all()
    q.filter("objId =", objId)
    q.filter("owner =", self.entryDbOwer)
    q.filter("dbId =", self.entryDbId)
    q.filter("keyId =", keyId)
    q.filter("valueId =", valueId)
    q.filter("valid =", True)
    #q.order("__key__")
    q.order('-modifiedDate')
    results = q.fetch(10)
    #print keyId, valueId
    '''
    for p in results:
      # u = ufsEntry(
        # owner = p.owner,
        # dbId = p.dbId,
        # objId = p.objId,
        # keyId = p.keyId,
        # valueId = p.valueId,
        # createdDate = p.createdDate,
        # createApp = p.createApp,
        # version = currentGaeEntryDbVersion)
      p.keyId = keyId
      p.valueId = valueId
      p.put()
      return
    '''
    for p in results:
      #print p.objId
      p.valid = False
      p.put()

  def hasKey(self, keyId):
    pass
  def runInTransaction(self, f):
    pass
