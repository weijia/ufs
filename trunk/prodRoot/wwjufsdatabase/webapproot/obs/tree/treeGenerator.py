import os
import urllib


class treeItemReadonly:
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

  def getContainer(self, relativeP):
    '''
    Get the container of this container
    '''
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    return directoryContainer(fullP)
    '''


class treeItem(treeItemReadonly):
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
    
  def mkContainer(self, relativeP):
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    if os.path.exists(fullP):
      return
    os.mkdir(fullP)
    '''

class dirTreeDataBase(treeItem):
  def getChildType(self, relativeP):
    '''
    Get the type of the item for the item identified with relativeP
    '''
    pass

    
    
    
class dirTreeData(dirTreeDataBase):
  def __init__(self, itemPath):
    '''
    The absolute path this item
    '''
    self.itemPath = itemPath
  def isThisAContainer(self):
    '''
    Check if this item is a container
    '''
    return os.path.isdir(self.itemPath)
  def getChildAbsPath(self, relativeP):
    '''
    Return the abs path of the child
    '''
    newP = os.path.join(self.itemPath, relativeP)
    return newP.replace('\\','/')
  def isContainer(self, relativeP):
    '''
    Check if the relative path is a container
    '''
    #print '%s is dir:'%os.path.join(self.itemPath, relativeP), os.path.isdir(os.path.join(self.itemPath, relativeP))
    #return os.path.isdir(os.path.join(self.itemPath, relativeP))
    if self.getChildType(relativeP) is None:
      return True
    
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
    for i in os.listdir(self.itemPath):
      l.append(i)
    return l

  def containerName(self):
    '''
    Get the container name
    '''
    '''
    return deStr(formattedDirectory.basename(self.p))
    '''
    import formattedDirectory
    return formattedDirectory.basename(self.itemPath)
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


  def getContainer(self, relativeP):
    '''
    Get the container of this container
    '''
    '''
    fullP = os.path.join(self.p, enStr(relativeP))
    return directoryContainer(fullP)
    '''
    return dirTreeData(formattedDirectory.dirname(self.itemPath))
  def getChildType(self, relativeP):
    '''
    Get the type of the item for the item identified with relativeP
    '''
    if len(relativeP.split('.')) > 1:
      return relativeP.split('.')[1]
    else:
      return None
    
def dirlist(treeItemToPopulate):
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       #d=urllib.unquote(request.POST.get('dir','c:\\temp'))
       for f in treeItemToPopulate.listChildren():
           ff=treeItemToPopulate.getChildAbsPath(f)
           if treeItemToPopulate.isContainer(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (urllib.quote(ff),urllib.quote(f)))
           else:
               e=treeItemToPopulate.getChildType(ff)
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (urllib.quote(e),urllib.quote(ff),urllib.quote(f)))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return ''.join(r)

   
   
   
def main():
  print dirlist(dirTreeData('d:/tmp'))
  
if __name__=="__main__":
  main()