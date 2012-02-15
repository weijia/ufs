try:
    import psyco
    psyco.full()
except ImportError:
    #print 'error'
    pass


import libSys
import libs.tag.tagSystemV2 as tagSystem
import urllib
import libs.html.response
import libs.http.queryParam
import os
from libs.utils.transform import *
#import collectionIteratorV2
import uuid

class tmpLog:
    def __init__(self):
        self.s = ''
    def l(self, s):
        self.s += s+'<br/>'

import sys
def fileIter(fullPath):
    for i in os.listdir(fullPath):
        try:
            #print >>sys.stderr, "reading dir:"+i
            yield unicode(i)
        except KeyError:
            #print >>sys.stderr, "key error"
            continue
            
def localDirCollectionIter(fullPath, start, cnt, loggerObj):
    realCnt = -1
    for i in os.listdir(fullPath):
        realCnt += 1
        if realCnt < start:
            continue
        if realCnt >= start+cnt:
            break
        try:
            yield unicode(i)
        except KeyError:
            continue

def collectionListItem(iter, divClassName = u"thumbDiv", imgClass=u"thumbImage", tagName=u"li"):
    thumbViewScript = u"http://localhost:8803/thumb?path="
    res = ""
    for i in iter:
        res +=u'<%s class="%s">'%(tagName, divClassName+ " ui-widget-content")
        t = tagSystem.tagSystemShoveDb()
        tList = t.getTags(i)
        tagStr = u""
        '''
        for k in tList:
            tagStr += k.decode('utf8')
        '''
        tagStr = u','.join(tList)
        '''
        res += '<div class="elementTag" path=%s>'%urllib.quote(i)
        res += ','.join(tList)
        res += 'default'
        res += '</div>'
        '''
        if tagStr == u"":
            tagStr = u"input tag"
        res += u'<img class="%s" src="%s%s" path="%s"/><p class="tagEditor">%s</p><div class="placeholder"></div>'%(imgClass, 
            thumbViewScript, urllib.quote(i.encode('gbk')), i, tagStr)#first encode the str, so the browser can decode the string to local encoding
        res += u'</%s>\n'%tagName
    return res
import sys
    
import libs.utils.stringTools as stringTools
def jsIdEncoding(s):
    '''
    This function is used to encode the item id of jstree as jstree can not manipulate id with ":" correctly
    '''
    l = s.split(u"_", 2)
    if len(l[0]) == 1:
        s = u":".join(l)
    return s

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorageUnicode()
    #fields = {}
    fullPath = fields.get("path", [u"c:/"])[0]
    fullPath = fullPath
    fullPath = jsIdEncoding(fullPath)
    #print >>sys.stderr, fullPath
    cnt = int(fields.get("cnt", [u"100"])[0])
    start = int(fields.get("start", [u"0"])[0])
    #fullPath = "d:/sys/pic"
    fullPath = transformDirToInternal(fullPath)
    h = libs.html.response.html()
    import libs.ufsDb.dictShoveDb as dictShoveDb

    collectionPreviewPathDb = dictShoveDb.getDbForDirCacheDb('collectionPreviewPathDb')
    collectionPreviewUuidDb = dictShoveDb.getDbForDirCacheDb('collectionPreviewUuidDb')
    try:
        u = unicode(collectionPreviewPathDb[fullPath])
        #h.write('existing one')
    except KeyError:
        u = unicode(uuid.uuid4())
        #h.write('create new')
        collectionPreviewPathDb[fullPath] = u
        collectionPreviewUuidDb[u] = fullPath
    l = tmpLog()
    iter = fileIter(fullPath)
    #fileList = localDirCollectionIter(fullPath, start, cnt, l)
    fileList = collectionIteratorV2.cachedCollectionIterFromRange(u, iter, start, cnt, l)
    h.genPartialHtmlHead()
    #h.write(str(i))
    co = []
    for k in fileList:
        p = transformDirToInternal(os.path.join(fullPath, k))
        co.append(p)


        
    #h.write('after calling')
    r = collectionListItem(co)
    h.write(r)
    #h.write(l.s)
    h.end()
