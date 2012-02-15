print "Content-Type: text/html;charset=utf-8"
print "hello world"

import libs.tree.dbTreeItem
import libs.platform.ufsDbManagerInterface
import uuid
import libs.http

testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

u = libs.platform.ufsDbManagerInterface.ufsUserExample('tester')

db = mngr.getSimpleDb(u, 'treeImporterDb')
i = libs.tree.dbTreeItem.dbTreeItem(testRoot, db)
ch1 = str(uuid.uuid4())
ch2 = str(uuid.uuid4())
i.addChild(ch1)
i.addChild(ch2)
print ch2
i = libs.tree.dbTreeItem.dbTreeItem(ch2, db)
ch2 = str(uuid.uuid4())
i.addChild(ch2)


