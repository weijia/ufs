import libs.tree.dbTreeItem
import uuid

class namedTreeItem(libs.tree.dbTreeItem.dbTreeItem):
  '''
  All items are only UUIDs. Need additional class to handle UUID to name conversion
  '''
  def __init__(self, itemId, treeDb, nameService, sequenceDb = None):
    '''
    The absolute path this item
    '''
    libs.tree.dbTreeItem.dbTreeItem.__init__(self, itemId, treeDb, sequenceDb)
    self.nameService = nameService
  def addNamedChild(self, relativePName, childId = None):
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    if os.path.exists(fullP):
      return
    os.mkdir(fullP)
    '''
    if childId is None:
        childId = str(uuid.uuid4())
    self.nameService.setName(childId, relativePName)
    self.addChild(childId)
    return childId
  def getName(self, id):
    n = self.nameService.getName(id)
    if n is None:
      return id
    return n
    
  def getChildName(self, id):
    n = self.nameService.getName(id)
    if n is None:
      return id
    return n
    
  def getItemName(self):
    n = self.nameService.getName(self.itemId)
    if n is None:
      return self.itemId
    return n
  def renameItemName(self, newName):
    self.nameService.updateName(self.itemId, newName)
    
  def appendNamedChild(self, relativePName):
    id = str(uuid.uuid4())
    self.nameService.setName(id, relativePName)
    self.appendChild(id)
    return id
  '''
  #The following function are not OK yet
  def insertChildAfterChild(self, relativeP, afterRelativeP):
    id = str(uuid.uuid4())
    self.nameService.setName(id, relativePName)
    self.addChild(id)
    return id
  '''