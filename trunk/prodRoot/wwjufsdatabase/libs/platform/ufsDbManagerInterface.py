class ufsUserInterface:
  def getMasterPasswd(self):
    pass
  def getUserId(self):
    pass

class ufsUserExample(ufsUserInterface):
  def __init__(self, username):
    self.username = username
  def getMasterPasswd(self):
    return self.username
  def getUserId(self):
    return self.username


class ufsDbManagerInterface:
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
    
    
class ufsDbManagerWithSystemDbProtectionInterface:
  def getSimpleDbInternal(self, user, dbName):
    pass
  def getComplexDbInternal(self, user, dbName):
    pass
  def getSimpleDbWithBigValueInternal(self, user, dbName):
    pass
    
