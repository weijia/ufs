#import libs.GAE.session
import libs.http.queryParam
import libs.platform.services
import libs.tree.jsTreeFunc
import libs.platform.ufsDbManagerInterface
import libs.tree.dbTreeItem

print "Content-Type: text/html;charset=utf-8"
print ""

q = libs.platform.services.getQueryService()
f = q.getAllFieldStorage()
#print f['sessionId']
#print f['sessionId'][0]

mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()
if f.has_key('username'):
  user = f['username'][0]
else:
  user = 'tester'
u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
if f.has_key('treeImporterDb'):
  dbName = f['treeImporterDb'][0]
else:
  dbName = 'treeImporterDb'
db = mngr.getSimpleDb(u, dbName)


if f['id'][0] == '0':
  print '''<li id = "%s" class="closed"><a href="#"><ins>&nbsp;</ins>/</a></li>
'''%f['treeRoot'][0]
else:
  #print '''<li id="%s" class="closed"><a href="#"><ins>&nbsp;</ins>%s</a></li><li><a href="#"><ins>&nbsp;</ins>Node 2</a></li>'''%(f, f['id'][0])
  d = f['id'][0]
  res = ''
  print '<!--'
  n = libs.tree.dbTreeItem.dbTreeItem(d, db)
  res = libs.tree.jsTreeFunc.dirlist(n)
  print '-->'
  #print res,d
  print res