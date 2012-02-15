# -*- coding: <utf8> -*-

import urllib
import libs.platform.services
import libs.utils.simplejson as json

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

import libs.utils.stringTools as stringTools
def jsIdEncoding(s):
    '''
    This function is used to encode the item id of jstree as jstree can not manipulate id with ":" correctly
    '''
    #return s
    l = s.split(u":", 1)
    if len(l[0]) == 1:
        s = "_".join(l)
    return s
import libs.utils.stringTools as stringTools
   
def containerList(treeItemToPopulate, content = None, itemClass = "jstree-closed", checkedItems = []):
    print 'list in dirlist:',treeItemToPopulate.listNamedChildren()
    en = libs.platform.services.getEncodingService()
    try:
        r=[]
        d = treeItemToPopulate.listNamedChildren()
        for f in d:
            itemId = f
            #not needed if jstree support ":"
            itemId = stringTools.jsIdEncoding(f)
            ff=treeItemToPopulate.getChildAbsPath(f)
            if content is None:
                i = u'<a href="#">%s</a>'%d[f]
            else:
                i = content%{'id':itemId, 'name':d[f]}
            #print 'before get is container'
            if itemId in checkedItems:
                itemClassWithCheckState = itemClass + " jstree-checked"
            else:
                itemClassWithCheckState = itemClass
            if treeItemToPopulate.isContainer(ff):
                r.append(u'<li id="%s" class="%s">%s</li>' % (itemId,itemClassWithCheckState,i))
            else:
                #e=treeItemToPopulate.getChildType(ff)
                r.append(u'<li id="%s">%s</li>' % (itemId,i))
            #break
    except IOError:#Exception,e:
        r.append(u'<li id="%s" class="jstree-closed">Could not load directory: %s</a></li>' % str(e))
    return u''.join(r)


def containerListJson(treeItemToPopulate, checkedItems = []):
    #print 'list in dirlist:',treeItemToPopulate.listNamedChildren()
    en = libs.platform.services.getEncodingService()
    r=[]
    try:
        d = treeItemToPopulate.listNamedChildren()
        for f in d:
            #print f, r
            itemId = f
            #not needed if jstree support ":"
            itemId = stringTools.jsIdEncoding(f)
            ff=treeItemToPopulate.getChildAbsPath(f)
            #print 'before get is container'
            
            if itemId in checkedItems:
                item["class"] = "jstree-checked"
            else:
                item = {}
            item["attr"] = {"id":itemId}
            item["data"] = d[f]
            item["fullPath"] = f
            if treeItemToPopulate.isContainer(ff):
                #r.append(u'<li id="%s" class="%s">%s</li>' % (itemId,itemClassWithCheckState,i))
                item["children"] = []
                item["state"] = "closed"

            r.append(item)
           #break
    except IOError:#Exception,e:
        r.append(u'<li id="%s" class="jstree-closed">Could not load directory: %s</a></li>' % str(e))
    #print json.dumps(r, indent = 4)
    return json.dumps(r, indent = 4)
