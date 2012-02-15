class jsTreeItemInterface:
  '''
  This interface should be implemented if use containerList to generate a jstree node
  '''
  def listNamedChildren(self, start = 0, cnt = None, getParent = True):
    pass
  def getChildAbsPath(self, relativePath):
    pass
  def isContainer(self, fullPath):
    pass

class readOnlyTreeItemInterface:
  def __init__(self, containerPath):
    '''
    The absolute path this item
    '''
    pass
  def isItemAContainer(self):
    '''
    Check if this item is a container
    '''
    pass
  def getItemAbsPath(self):
    pass
  def getChildAbsPath(self, relativeP):
    '''
    Return the abs path of the child
    '''
    pass
  def isContainer(self, relativeP):
    '''
    Check if the relative path is a container
    '''
    pass
    
  def listChildren(self):
    '''
    Return a list of children for this container
    '''
    '''
    l = []
    for i in os.listdir(self.p):
      l.append(deStr(i))
    return l
    '''

  def containerName(self):
    '''
    Get the container name
    '''
    '''
    return deStr(formattedDirectory.basename(self.p))
    '''
  '''
  def getItems(self, relativeP):
    #Same as listChildren?
    fullP = os.path.join(self.p, enStr(relativeP))
    print 'opening list file: %s'%fullP
    f = open(fullP, 'r')
    ls = f.readlines()
    f.close()
    return ls
  '''

  def getContainer(self):
    '''
    Get the container of this container
    '''
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    return directoryContainer(fullP)
    '''
    #The above example seems incorrect

class treeItemInterface(readOnlyTreeItemInterface):
  def renameItem(self, originalRelativeP, newRelativeP):
    '''
    Rename the item
    '''
    '''
    fullOP = os.path.join(self.p, enStr(originalRelativeP))
    fullNP = os.path.join(self.p, enStr(newRelativeP))
    print 'renaming:"%s" to:"%s"'%(fullOP, fullNP)
    if fullOP == fullNP:
      return
    if os.path.exists(fullNP):
      print 'duplicated directories texts'
      return
    os.rename(fullOP, fullNP)
    '''
    
  # def mkContainer(self, relativeP):
    # '''
    # fullP = os.path.join(self.p, enStr(relativeP))
    # if os.path.exists(fullP):
      # return
    # os.mkdir(fullP)
    # '''
  def addChild(self, relativeP):
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    if os.path.exists(fullP):
      return
    os.mkdir(fullP)
    '''
    pass