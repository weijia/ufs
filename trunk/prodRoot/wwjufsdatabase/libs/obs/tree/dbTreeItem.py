from treeItemInterface import treeItemInterface

sysChildAttr = 'sys_child'
sysTreeTag = 'sys_tag_tree'
sysTagAttr = 'sys_tag'
sysChildSequenceListAttr = 'sys_child_sequence_list'
sysGlobalTreeRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'

class dbTreeItem(treeItemInterface):
  '''
  All items are only UUIDs. Need additional class to handle UUID to name conversion
  '''
  def __init__(self, itemId, treeDb, sequenceDb = None):
    '''
    The absolute path this item
    '''
    self.treeDb = treeDb
    self.itemId = itemId
    #The sequenceDb parameter is a storage db, it will contain the sequence of children
    if sequenceDb is None:
      self.sequenceDb = self.treeDb
    else:
      self.sequenceDb = sequenceDb
  def getItemAbsPath(self):
    return self.itemId
  def isItemAContainer(self):
    '''
    Check if this item is a container
    '''
    n = self.treeDb.getAttrList(self.itemId, sysChildAttr)
    if len(n) > 0:
      return True
    return False
  def getChildAbsPath(self, relativeP):
    '''
    Return the abs path of the child
    '''
    return relativeP
  def isContainer(self, relativeP):
    '''
    Check if the relative path is a container
    '''
    n = self.treeDb.getAttrList(relativeP, sysChildAttr)
    if len(n) > 0:
      return True
    return False

    
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
    l = []
    n = self.treeDb.getAttrList(self.itemId, sysChildAttr)
    cnt = 0
    #print n
    l.extend(n)
    while False:#(len(n) > 0) and (cnt<1):
      l.extend(n)
      cnt += 1
      n = self.treeDb.getAttrList(self.itemId, sysChildAttr)
    return l
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
    n = self.treeDb.getObjIdList(sysChildAttr, self.itemId)
    #print n
    if len(n) > 0:
      return n[0]
    else:
      return None
  def getChildType(self, relativeP):
    return 'txt'
    
  def addChild(self, relativeP):
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    if os.path.exists(fullP):
      return
    os.mkdir(fullP)
    '''
    self.treeDb.add(self.itemId, sysChildAttr, relativeP)
    self.treeDb.add(self.itemId, sysTagAttr, sysTreeTag)
  '''
  #This fuction is not needed
  def addChildSequence(self, childList):
    self.treeDb.add(self.itemId, sysChildSequenceListAttr, ','.join(childList))
  '''
  def listSortedChildren(self):
    '''
    Return a list of children for this container
    '''
    '''
    l = []
    for i in os.listdir(self.p):
      l.append(deStr(i))
    return l
    '''
    l = []
    n = self.treeDb.getAttrList(self.itemId, sysChildAttr)
    s = self.sequenceDb.getAttrList(self.itemId, sysChildSequenceListAttr)
    #print s
    if len(s) != 0:
      s = s[0].split(',')
    else:
      s = []
    cnt = 0
    #print n
    l.extend(n)
    for i in s:
      try:
        l.index(i)
      except:
        s.remove(i)
    for i in l:
      try:
        s.index(i)
      except:
        s.append(i)
    return s
  
  
  def updateSequence(self, childSequenceList):
    s = self.sequenceDb.getAttrList(self.itemId, sysChildSequenceListAttr)
    o = ','.join(childSequenceList)
    if len(s) > 0:
      self.sequenceDb.update(self.itemId, sysChildSequenceListAttr, s[0], o)
    else:
      self.sequenceDb.add(self.itemId, sysChildSequenceListAttr, o)

      
  '''
  def appendChild(self, relativeP):
    self.addChild(relativeP)
    s = self.sequenceDb.getAttrList(self.itemId, sysChildSequenceListAttr)
    if len(s) != 0:
      #print s
      n = s[0].split(',')
      n.append(relativeP)
      self.sequenceDb.update(self.itemId, sysChildSequenceListAttr, s[0], ','.join(n))
    else:
      s = [relativeP]
      self.sequenceDb.add(self.itemId, sysChildSequenceListAttr, ','.join(s))

  def insertChildAfterChild(self, relativeP, afterRelativeP):
    s = self.treeDb.getAttrList(self.itemId, sysChildSequenceListAttr)
    if len(s) != 0:
      s = s[0].split(',')
      try:
        i = s.index(afterRelativeP)
        s.insert(i, relativeP)
      except:
        s.extend([afterRelativeP, relativeP])
      self.treeDb.update(self.itemId, sysChildSequenceListAttr, ','.join(s))
    else:
      s = [afterRelativeP, relativeP]
      self.treeDb.add(self.itemId, sysChildSequenceListAttr, ','.join(s))
  '''
  def delete(self):
    c = self.getContainer()
    if c is None:
      pass
    else:
      self.treeDb.delete(c, sysChildAttr, self.itemId)
