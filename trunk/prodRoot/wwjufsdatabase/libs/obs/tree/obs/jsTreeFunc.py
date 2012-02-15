
import urllib

def dirlist(treeItemToPopulate):
   #print 'list in dirlist:',treeItemToPopulate.listChildren()
   try:
       r=[]
       #d=urllib.unquote(request.POST.get('dir','c:\\temp'))
       for f in treeItemToPopulate.listChildren():
           ff=treeItemToPopulate.getChildAbsPath(f)
           if treeItemToPopulate.isContainer(ff):
               r.append('<li id="%s" class="closed"><a href="#"><ins>&nbsp;</ins>%s</a></li>' % (urllib.quote(f),urllib.quote(f)))
           else:
               #e=treeItemToPopulate.getChildType(ff)
               r.append('<li id="%s"><a href="#"><ins>&nbsp;</ins>%s</a></li>' % (urllib.quote(f),urllib.quote(f)))
           #break
   except Exception,e:
       r.append('<li><a href="#"><ins>&nbsp;</ins>Could not load directory: %s</a></li>' % str(e))
   return ''.join(r)
