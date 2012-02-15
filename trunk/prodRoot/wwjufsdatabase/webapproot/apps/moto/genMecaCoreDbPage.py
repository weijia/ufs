from libs.services.services import services
gMenuDbHeader = '''<br/>;*******************************************************************************<br/>
; TEST MENU FILE<br/>
;*******************************************************************************<br/>
'''

s = services()
gEof = '\n'
gEof = '<br/>'

def generateMecaCoreDb(container, dbFileHandle, isRootItem = False):
  '''
  container will be scaned and sub-directories will be
  '''
  parentName = container.getItemName()#Here, whatever the directory is end with '/', the basename is always not ''.
  if isRootItem:
    #Generate a file header. It is just a description of the test menu file
    dbFileHandle.write(gMenuDbHeader)
    dbFileHandle.write('$Main = %s%s'%(parentName, gEof))
  childrenList = container.listSortedChildren()#itemEnumFunc(container, isRootItem)
  #childrenList.sort()
  #print childrenList
  dbFileHandle.write('#%s = %d%s'%(parentName, len(childrenList), gEof))
  #InDir Find all directories in this dir
  cnt = 1
  il = []
  for i in childrenList:
    n = s.getTreeItem('treeImporterDb','treeImporterNameDb',i,'treeImporterBigValueDb')
    il.append(n)
    dbFileHandle.write('$%s %%%d = %s%s'%(parentName, cnt, n.getItemName(), gEof))
    cnt += 1
    if False:
        if cnt > 6:
            break
  dbFileHandle.write(gEof)
  for i in il:
    if i.isItemAContainer():
      generateMecaCoreDb(i, dbFileHandle, False)
    else:
      dbFileHandle.write('#%s = %d%s'%(i.getItemName(), 0, gEof))


'''
genMecaCoreDbPage.py?username=tester&treeRoot=
'''

h = s.getHtmlGen()
h.genHead()
r = s.getParam('treeRoot', s.getDefaultTreeRoot())
i = s.getTreeItem('treeImporterDb','treeImporterNameDb',r,'treeImporterBigValueDb')
generateMecaCoreDb(i, h, isRootItem = True)

h.genEnd()