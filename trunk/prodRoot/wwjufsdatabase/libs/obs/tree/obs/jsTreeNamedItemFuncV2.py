# -*- coding: <utf8> -*-

import urllib
import libs.platform.services

def dirlist(treeItemToPopulate, content = None):
   #print 'list in dirlist:',treeItemToPopulate.listSortedChildren()
   en = libs.platform.services.getEncodingService()
   try:
       r=[]
       #d=urllib.unquote(request.POST.get('dir','c:\\temp'))
       for f in treeItemToPopulate.listSortedChildren():
           #print 'before get abs'
           ff=treeItemToPopulate.getChildAbsPath(f)
           #print 'before get name'
           #n = en.en(treeItemToPopulate.getName(f))
           n = treeItemToPopulate.getName(f)
           if content is None:
              i = u'<a href="#">%s</a>'%n
           else:
              i = content%{'id':f, 'name':n}
           #print 'before get is container'
           if treeItemToPopulate.isContainer(ff):
               r.append(u'<li id="%s" class="jstree-closed">%s</li>' % (f,i))
           else:
               #e=treeItemToPopulate.getChildType(ff)
               r.append(u'<li id="%s">%s</li>' % (f,i))
           #break
   except IOError:#Exception,e:
       r.append(u'<li><a href="#">Could not load directory: %s</a></li>' % str(e))
   return en.en(u''.join(r))

   
   
def containerList(treeItemToPopulate, content = None, itemClass = "jstree-closed"):
   #print 'list in dirlist:',treeItemToPopulate.listNamedChildContainer()
   en = libs.platform.services.getEncodingService()
   try:
       r=[]
       d = treeItemToPopulate.listNamedChildContainer()
       for f in d:
           ff=treeItemToPopulate.getChildAbsPath(f)
           if content is None:
              i = u'<a href="#">%s</a>'%d[f]
           else:
              i = content%{'id':f, 'name':d[f]}
           #print 'before get is container'
           if treeItemToPopulate.isContainer(ff):
               r.append(u'<li id="%s" class="%s">%s</li>' % (f,itemClass,i))
           else:
               #e=treeItemToPopulate.getChildType(ff)
               r.append(u'<li id="%s">%s</li>' % (f,i))
           #break
   except IOError:#Exception,e:
       r.append(u'<li id="%s" class="jstree-closed">Could not load directory: %s</a></li>' % str(e))
   return en.en(u''.join(r))
