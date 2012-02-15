sysNameAttr = 'sys_name'

class nameService:
  '''
  All items are only UUIDs. Need additional class to handle UUID to name conversion
  '''
  def __init__(self, nameDb):
    self.nameDb = nameDb

    
  def getName(self, id):
    n = self.nameDb.getAttrList(id, sysNameAttr)
    if len(n) > 0:
      return n[0]
      #sreturn ','.join(n)
    return None
    
  def getNames(self, id):
    n = self.nameDb.getAttrList(id, sysNameAttr)
    if len(n) > 0:
      #return n[0]
      return ','.join(n)
    return None


  def setName(self, id, name):
    self.nameDb.add(id, sysNameAttr, name)
    
    
  def updateName(self, id, name):
    oldName = self.getName(id)
    if oldName is None:
      print 'create name for:',id
      self.setName(id, name)
    else:
      print 'updating name'
      self.nameDb.update(id, sysNameAttr, oldName, name)
