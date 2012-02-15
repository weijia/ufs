sysNameAttr = 'sys_name'

class nameService:
  '''
  All items are only UUIDs. Need additional class to handle UUID to name conversion
  '''
  def __init__(self, nameDb):
    self.nameDb = nameDb

    
  def getName(self, id):
    try:
      n = self.nameDb[id]
    except KeyError:
      return None
    if len(n) > 0:
      return n[0]
      #sreturn ','.join(n)
    return None
    
  def getNames(self, id):
    n = self.nameDb[id]
    if len(n) > 0:
      #return n[0]
      return ','.join(n)
    return None


  def setName(self, id, name):
    self.nameDb.append(id, name)
    
    
  def updateName(self, id, name):
    del self.nameDb[id]
    self.nameDb.append(id, name)
