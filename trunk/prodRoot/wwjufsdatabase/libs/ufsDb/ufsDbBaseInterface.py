class ufsDbTokenDbInterface:
  def __init__(self, owner, dbId):
    pass
  def get(self, tokenId):
    pass
  def getId(self, token):
    pass

class ufsSimpleDbEntryDbInterface:
  def __init__(self, entryDbOwer, entryDbId):
    pass
  def getObjIdList(self, keyId, valueId, offset = 0, limit = 20):
    pass
  def add(self, objId, keyId, valueId, createapp):
    pass
  def update(self, objId, keyId, valueId, newValue):
    pass
  def hasKey(self, keyId):
    pass
  def delete(self, objId, keyId, valueId):
    pass
  def runInTransaction(self, f):
    pass

class ufsDbEntryDbInterface(ufsSimpleDbEntryDbInterface):
  def getObjIdListAllCondition(self, keyValuePair, offset = 0, limit = 20):
    pass
  def getObjIdListOneCondition(self, keyValuePair, offset = 0, limit = 20):
    pass
    
class ufsSimpleDbBaseInterface:
  # def __init__(self, tokenDb, entryDb):
    # pass
  def add(self, objId, key, value, createapp):
    pass
  def getAttr(self, objId, k):
    pass
  def update(self, objId, key, value, newValue):
    pass
  def getObjIdList(self, key, value, offset = 0, limit = 20):
    pass
  def getAttrList(self, objId, key, offset = 0, limit = 20):
    pass
  def run_in_transaction(self, f):
    pass
    
    
class ufsDbBaseInterface(ufsSimpleDbBaseInterface):
  def getObjIdListAllCondition(self, keyValuePair, offset = 0, limit = 20):
    pass
  def getObjIdListOneCondition(self, keyValuePair, offset = 0, limit = 20):
    pass

class ufsDbTextStorageInterface:
  def storeData(self, key, data, createapp):
    pass
  def getData(self, key):
    pass