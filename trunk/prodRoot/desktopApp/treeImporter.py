import urllib
import libSys
#import libs.platform.ufsDbManagerInterface.ufsUserExample
import libs.platform.ufsDbManagerInterface
import libs.tree.dbTreeItem

#u = libs.platform.ufsDbManagerInterface.ufsUserExample('tester')
import libs.ufsDb.ufsClient

u = libs.ufsDb.ufsClient.ufsClient()
u.login('tester', 'testpass')
print u.sid

m = libs.platform.ufsDbManagerInterface.ufsDbManager()
db = m.getSimpleDbClient(u, 'treeImporterDb')

testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'


nameDb = mngr.getSimpleDbClient(u, 'treeImporterNameDb')
nS = libs.services.nameService.nameService(nameDb)

root = libs.tree.namedTreeItem.namedTreeItem(testRoot, db, nS)

importToFile(inputFile, i)

import string
import uuid

def importFile(inputFile, root)
  mecacoreRoot = str(uuid.uuid4())
  mecacoreRootId = i.appendNamedChild(mecacoreRoot+'mecacoreRoot')
  mecaCoreMain = libs.tree.namedTreeItem.namedTreeItem(mecacoreRootId, db, nS)
  nameHash = {'$Main': mecaCoreMain}#{Name: item ID}
  for i in inputFile.readlines():
    l = i.split('=')
    left = strip(l[0])
    right = strip(l[1])
    if left[0] == ';'
      continue
    if left[0]=='$':
      #$TDD Test Menu %1 = XXXXXX
      #$TDD Test Menu %2 = YYYYYY
      parent = string.strip(left.split('%')[0])
      child = string.strip(right)
      n = libs.tree.namedTreeItem.namedTreeItem(nameHash[parent], db, nS).appendNamedChild(child)
      nameHash[child] = n