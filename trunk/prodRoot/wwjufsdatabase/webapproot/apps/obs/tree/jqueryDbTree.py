if False:
  print "Content-Type: text/html;charset=utf-8"
  print "hello world"

print '<!--good'
import libs.http.queryParam
import libs.platform.services
import libs.tree.dbTreeItem
import libs.tree.jsFileTreeFunc
import libs.platform.ufsDbManagerInterface
#import os
import sys
import urllib


q = libs.platform.services.getQueryService()
f = q.getAllFieldStorage()

testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
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
i = libs.tree.dbTreeItem.dbTreeItem(testRoot, db)

#print f

res = ''
if f.has_key('dir'):
  if f['dir'][0] == '/':
    res = libs.tree.jsFileTreeFunc.dirlist(libs.tree.dbTreeItem.dbTreeItem(testRoot, db))
  else:
    d = urllib.unquote(f['dir'][0]).split('/')[-2]#The parameter will be dir1/dir2/ etc. just like filesyetem, with a '/' at the end
    if True:
      res = libs.tree.jsFileTreeFunc.dirlist(libs.tree.dbTreeItem.dbTreeItem(d, db))
      print res,d
    else:
      '''
      The following codes are just used to output debug info
      '''
      #print 
      #raise 'bad'
      #print >>sys.stderr,f
      res += '<ul class="jqueryFileTree" style="display: none;">'
      res += '<li class="directory collapsed><a href="#" rel="%s/">%s</a>'%(d,d)
      #print f
      #print 'environment:',os.environ.get('QUERY_STRING','')
      #print sys.stdin.read()
      res += '</li>'
      res += '</ul>'
else:
  i = libs.tree.dbTreeItem.dbTreeItem(testRoot, db)
  res = libs.tree.jsFileTreeFunc.dirlist(i)
  pass
print '-->'
print res