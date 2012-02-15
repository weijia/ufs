import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *

import collectionIterator

    
def showThumbCollection(iter, divClassName = "thumbDiv", imgClass="thumbImage"):
    #thumbViewScript = "picList.py?path="
    #thumbViewScript = "http://localhost:8802/webapproot/apps/localServer/thumb.py?path="
    thumbViewScript = "http://localhost:8803/thumb?path="
    res = ""
    for i, thumbPath in iter:
        res +='<div class="%s">'%divClassName
        if i != thumbPath:
            res += '<img class="%s" src="%s%s" width="100px" height="100px" path="%s"/>'%(imgClass, thumbViewScript, 
                urllib.quote(thumbPath),urllib.quote(i))
        else:
            res += '<img class="%s" src="%s%s" width="100px" height="100px" path="%s"/>'%(imgClass, thumbViewScript, urllib.quote(thumbPath),
                urllib.quote(i))
        res += '</div>\n'
    return res

    
def showCollection(h, i, path, page = None):
    if page is None:
        h.inc('/webapproot/js/development-bundle/jquery-1.4.2.js')
        h.inc('/webapproot/js/development-bundle/ui/jquery-ui-1.8.2.custom.js')
        h.inc('/webapproot/js/standalone/jquery.livequery.js')
        h.inc('/webapproot/js/standalone/jquery.lazyload.js')
        h.inc('/webapproot/js/custom/pageAutoLoad.js')
        h.write('<link rel="stylesheet" type="text/css" href="/webapproot/static/css/class.css" />')
        h.write('<link rel="stylesheet" type="text/css" href="http://localhost:8801/webapproot/js/jstree/themes/default/style.css" />')

        h.write('<div id="log"></div>')
        h.write('<script type="text/javascript">\n')
        h.write('$(function(){$("#collectionList").autoPager({nextPageUrl:"%s"});});\n'%("collectionV6.py?path="+path.replace('\\','\\\\')+"&page="))
        h.write('</script>\n')
        h.write('<div id="collectionList" style="max-height:100%;overflow-y:scroll;">')
    else:
        h.write('<div>')
    h.write(showThumbCollection(i))
    #h.write('before gen end')
    h.write('</div>')
    
class tmpLog:
    def __init__(self):
        self.s = ''
    def l(self, s):
        self.s += s
        
        
def fileIter(fullPath):
    for i in os.listdir(fullPath):
        try:
            p = os.path.join(fullPath, i)
            if not os.path.isdir(p):
                yield i.decode("gb2312")
        except UnicodeDecodeError:
            continue

import shove
import collectionIteratorV2
import uuid

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    fullPath = fields["path"][0]
    fullPath = transformDirToInternal(fullPath)
    h = libs.html.response.html()

    gAppPath = 'd:/tmp/fileman/'
    gDbPath = os.path.join(gAppPath, 'db')


    libs.utils.misc.ensureDir(gDbPath)
    collectionPreviewPathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewPathDb.sqlite'))
    collectionPreviewUuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewUuidDb.sqlite'))
    try:
        u = collectionPreviewPathDb[fullPath]
        #h.write('existing one')
    except KeyError:
        u = str(uuid.uuid4())
        #h.write('create new')
        collectionPreviewPathDb[fullPath] = u
        collectionPreviewUuidDb[u] = fullPath
    iter = fileIter(fullPath)
    l = tmpLog()
    #h.write(fullPath)
    page = fields.get("page",[None])[0]
    #h.write(str(page))
    thumbPerLine = int(fields.get("thumbPerLine", [5])[0])
    #h.write('calling album')
    if page is None:
        realPage = 0
    else:
        page = int(page)
        realPage = page
    i = collectionIteratorV2.cachedCollectionIter(u, iter, realPage, l)
    co = []
    for k in i:
        p = os.path.join(fullPath, k)
        co.append([p, p])

    #h.write('after calling')
    h.genHead('Collections')
    showCollection(h, co, fullPath, page)
    #h.write(l.s)
    h.genEnd()
