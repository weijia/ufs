# -*- coding: <utf8> -*-

import urllib
#import libs.platform.services
import libs.utils.simplejson as json
import libs.utils.stringTools as stringTools
import libs.tag.tagSystemInterface as tagSys
import libs.utils.encodingTools as encodingTools

class listJsonInterface:
    def listNamedChildren(self, start, cnt, isTree):
        pass
    def getChildAbsPath(self, child):
        pass
    def isChildContainer(self, child):
        pass


def containerListJson(treeItemToPopulate, start, cnt, isTree = False, req = None, checkedItems = []):
    #print 'list in dirlist:',treeItemToPopulate.listNamedChildren()
    #en = libs.platform.services.getEncodingService()
    r=[]
    try:
        d = treeItemToPopulate.listNamedChildren(start, cnt, isTree)
        for f in d:
            #print f, r
            itemId = f
            #not needed if jstree support ":"
            itemId = stringTools.jsIdEncoding(f)
            ff=treeItemToPopulate.getChildAbsPath(f)
            #print 'before get is container'
            encoded = urllib.quote(encodingTools.translateToPageEncoding(f))
            if itemId in checkedItems:
                item["class"] = "jstree-checked"
            else:
                item = {}
            item["attr"] = {"id":itemId}
            item["data"] = d[f]
            item["fullPath"] = f
            item["utf8FullPath"] = encoded
            if treeItemToPopulate.isContainer(ff):
                #r.append(u'<li id="%s" class="%s">%s</li>' % (itemId,itemClassWithCheckState,i))
                item["children"] = []
                item["state"] = "closed"
            if not isTree:
                t = tagSys.getTagSysObj(req.getDbSys())
                tList = t.getTags(f)
                item["tags"] = tList
            r.append(item)
            #break
    except IOError:#Exception,e:
        r.append(u'<li id="%s" class="jstree-closed">Could not load directory: %s</a></li>' % str(e))
    #print json.dumps(r, indent = 4)
    return json.dumps(r, indent = 4)
