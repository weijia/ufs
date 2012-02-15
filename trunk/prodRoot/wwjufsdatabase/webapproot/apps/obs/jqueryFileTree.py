'''
print "Content-Type: text/plain"
print ""
print "Hello, world!"
'''
print '<!--good'
import libs.http.queryParam
import libs.platform.services
import webapproot.tree.treeGenerator
#import os
#import sys
import urllib


q = libs.platform.services.getQueryService()
f = q.getAllFieldStorage()
print f
print '-->'

if f.has_key('dir'):
  if True:
    print webapproot.tree.treeGenerator.dirlist(webapproot.tree.treeGenerator.dirTreeData(urllib.unquote(f['dir'][0])))
  else:
    print 
    print '<ul class="jqueryFileTree" style="display: none;">'
    print f
    #print 'environment:',os.environ.get('QUERY_STRING','')
    #print sys.stdin.read()
    print '</ul>'
else:
  print webapproot.tree.treeGenerator.dirlist(webapproot.tree.treeGenerator.dirTreeData('d:/'))

