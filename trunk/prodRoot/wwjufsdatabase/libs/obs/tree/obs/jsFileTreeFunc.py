
import urllib

def dirlist(treeItemToPopulate):
   print 'list in dirlist:',treeItemToPopulate.listChildren()
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
       #r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return ''.join(r)
