# -*- coding: <utf8> -*-

import urllib
#import libs.platform.services
import libs.utils.simplejson as json
import libs.utils.stringTools as stringTools
import libs.tag.tagSystemInterface as tagSys
import libs.utils.encodingTools as encodingTools

class listJsonInterface:
    def listNamedChildren(self, start, cnt, isTree):
        '''
        return an dictionary with res[fullPath] = name
        '''
        pass
    def isChildContainer(self, child):
        pass


def containerListJson(treeItemToPopulate, start, cnt, isTree = False, req = None, checkedItems = []):
    #print 'list in dirlist:',treeItemToPopulate.listNamedChildren(start, cnt, isTree)
    #en = libs.platform.services.getEncodingService()
    r=[]
    dbSys = req.getDbSys()
    t = tagSys.getTagSysObj(dbSys)
    try:
        d = treeItemToPopulate.listNamedChildren(start, cnt, isTree)
        for f in d:
            #print f, r
            itemId = f
            #not needed if jstree support ":"
            itemId = stringTools.jsIdEncoding(f)
            #print 'before get is container'
            encoded = urllib.quote(encodingTools.translateToPageEncoding(f))
            item = {}
            if itemId in checkedItems:
                item["class"] = "jstree-checked"
            else:
                item = {}
            item["attr"] = {"id":itemId}
            item["data"] = d[f]
            item["fullPath"] = f
            item["utf8FullPath"] = encoded
            if treeItemToPopulate.isChildContainer(f):
                #r.append(u'<li id="%s" class="%s">%s</li>' % (itemId,itemClassWithCheckState,i))
                item["children"] = []
                item["state"] = "closed"
            if not isTree:
                #print f
                #print 'getting tree --------------------------', f
                try:
                    tList = t.getTags(f)
                except:
                    tList = []
                item["tags"] = tList
            r.append(item)
            #break
    except IOError, e:#Exception,e:
        item = {}
        item["data"] = str(e)
        r.append(item)
    #print json.dumps(r, indent = 4)
    return json.dumps(r, indent = 4)
