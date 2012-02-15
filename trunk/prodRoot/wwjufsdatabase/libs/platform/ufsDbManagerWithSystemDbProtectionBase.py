import ufsDbManagerInterface as ufsDbManagerInterface
import ufsDbManagerInterface.ufsUserExample as ufsUserExample

class creatingUserDatabaseWithSystemDefinedDatabaseName: pass
class creatingSystemDatabaseWithUserDefinedDatabaseName: pass

systemDbNameListDbName = u"systemDbNameListDb"
systemDbNameListObjId = u'57fc1362-3ed0-4feb-b0fc-eb733a3841c3'
systemDbNameListObjNameListAttr = "dbListAttr"
userDbNameListObjId = u'916e846a-4da3-4aae-9957-e35645ab2e60'
systemDbNameList = [systemDbNameListDbName]
systemDbType = "SystemDbType"
userDbType = "userDbType"
undefinedDbType = "undefinedDbType"
    
class ufsDbManagerWithSystemDbProtectionBase(ufsDbManagerWithSystemDbProtectionInterface,ufsDbManagerInterface):
  def getSystemSimpleDb(self, dbName):
    u = ufsUserExample.ufsUserExample('richard.system')
    if self.checkDbName() == userDbType:
        raise creatingDatabaseWithSystemDefinedDatabaseName
    self.addSystemDbName(dbName)
    return self.getSimpleDbInternal(u, dbName)

  def getSystemComplexDb(self, dbName):
    u = ufsUserExample.ufsUserExample('richard.system')
    if self.checkDbName() == userDbType:
        raise creatingDatabaseWithSystemDefinedDatabaseName
    self.addSystemDbName(dbName)
    return self.getComplexDbInternal(u, dbName)
  def addSystemDbName(self, dbName):
    db = self.getSimpleDbInternal(ufsUserExample.ufsUserExample('richard.system'), systemDbNameListDbName)
    db.add(systemDbNameListObjId, systemDbNameListObjNameListAttr, dbName)
  def addUserDbName(self, dbName):
    db = self.getSimpleDbInternal(ufsUserExample.ufsUserExample('richard.system'), systemDbNameListDbName)
    db.add(userDbNameListObjId, systemDbNameListObjNameListAttr, dbName)
    
  def checkDbName(self, dbName):
    if dbName in systemDbNameList:
        return systemDbType
    db = self.getSimpleDbInternal(ufsUserExample.ufsUserExample('richard.system'), systemDbNameListDbName)
    if len(db.getObjIdList(systemDbNameListObjNameListAttr, dbName)) > 0:
        #It is a system db
        return systemDbType
    elif len(db.getObjIdList(userDbNameListObjId, dbName)) > 0:
        #It is a user db
        return userDbType
    #The name not ocuppied
    return undefinedDbType
    
  def getSimpleDb(self, user, dbName):
    if self.checkDbName() == systemDbType:
        raise creatingSystemDatabaseWithUserDefinedDatabaseName
    self.addUserDbName(dbName)
    return self.getComplexDbInternal(user, dbName)
  def getComplexDb(self, user, dbName):
    if self.checkDbName() == systemDbType:
        raise creatingSystemDatabaseWithUserDefinedDatabaseName
    self.addUserDbName(dbName)
    return self.getComplexDbInternal(user, dbName)
  def getSimpleDbWithBigValue(self, user, dbName):
    if self.checkDbName() == systemDbType:
        raise creatingSystemDatabaseWithUserDefinedDatabaseName
    self.addUserDbName(dbName)
    return self.getComplexDbInternal(user, dbName)
  '''
  def getSimpleDbInternal(self, user, dbName):
    pass
  def getComplexDbInternal(self, user, dbName):
    pass
  def getSimpleDbWithBigValueInternal(self, user, dbName):
    pass
  '''