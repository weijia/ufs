import ufsDbManagerInterface as ufsDbManagerInterface
import ufsDbManagerInterface.ufsUserExample as ufsUserExample
import ufsDbManagerWithSystemDbProtectionInterface
    
class ufsDbManager(ufsDbManagerWithSystemDbProtectionBase):
  '''
  The following function are implemented in ufsDbManagerWithSystemDbProtectionBase
  def getSimpleDb(self, user, dbName):
    pass
  def getComplexDb(self, user, dbName):
    pass
  def getSimpleDbWithBigValue(self, user, dbName):
    pass
  def getSystemSimpleDb(self, dbName):
    pass
  def getSystemComplexDb(self, dbName):
    pass
  '''
  
  def getSimpleDbInternal(self, user, dbName):
    try:
      import libs.GAE.ufsDbGaeTokenDb
      import libs.GAE.ufsDbGaeEntryDbV2
      import libs.ufsDb.ufsDbBase
    except:
      raise 'Can not import modules'
    t = libs.GAE.ufsDbGaeTokenDb.ufsDbGaeTokenDb(user.getUserId(),dbName)
    e = libs.GAE.ufsDbGaeEntryDbV2.ufsSimpleDbGaeEntryDb(user.getUserId(),dbName)
    return libs.ufsDb.ufsDbBase.ufsDbBase(t,e)
    
  def getSimpleDbWithBigValue(self, user, dbName):
    try:
      import libs.GAE.ufsDbGaeTokenDb
      import libs.GAE.ufsDbGaeEntryDbV2
      import libs.ufsDb.ufsDbBase
      import libs.GAE.ufsDbGaeStorage
      t = libs.GAE.ufsDbGaeTokenDb.ufsDbGaeTokenDb(user.getUserId(),dbName)
      v = libs.GAE.ufsDbGaeStorage.ufsDbGaeStorageTokenDb(user.getUserId(),dbName)
      e = libs.GAE.ufsDbGaeEntryDbV2.ufsSimpleDbGaeEntryDb(user.getUserId(),dbName)
      return libs.ufsDb.ufsDbBase.ufsDbBase(t,e,v)
    except:
      raise 'Can not import modules'

  def getSimpleDbClient(self, user, dbName):
    import libs.client.ufsSimpleDbBaseClient
    return libs.client.ufsSimpleDbBaseClient.ufsSimpleDbBaseClient(user, dbName)
    
  def getStorageDbClient(self, user, dbName):
    import libs.client.ufsStorageClient
    return libs.client.ufsStorageClient.ufsStorageClient(user, dbName)
    
  def getStorageDb(self, user, dbName):
    import libs.GAE.ufsDbGaeStorage
    return libs.GAE.ufsDbGaeStorage.ufsDbGaeStorage(user.getUserId(),dbName)
    
  def getComplexDbInternal(self, user, dbName):
    pass