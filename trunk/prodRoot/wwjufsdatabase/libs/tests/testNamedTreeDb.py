print "Content-Type: text/html;charset=utf-8"
print "hello world"

import libs.tree.namedTreeItem
import libs.platform.ufsDbManagerInterface
import uuid
import libs.http
import libs.services.nameService

testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

u = libs.platform.ufsDbManagerInterface.ufsUserExample('tester')

db = mngr.getSimpleDb(u, 'treeImporterDb')
nameDb = mngr.getSimpleDb(u, 'treeImporterNameDb')
nS = libs.services.nameService.nameService(nameDb)


i = libs.tree.namedTreeItem.namedTreeItem(testRoot, db, nS)
ch1 = str(uuid.uuid4())
ch2 = str(uuid.uuid4())
i.addNamedChild('first child')
ch2 = i.addNamedChild('second child')

i = libs.tree.namedTreeItem.namedTreeItem(ch2, db, nS)
i.addNamedChild('low level child')


