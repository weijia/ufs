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

        h.write('<div id="log"></div>')
        h.write('<script type="text/javascript">\n')
        h.write('$(function(){$("#collectionList").autoPager({nextPageUrl:"%s"});});\n'%("collectionV4.py?path="+path.replace('\\','\\\\')+"&page="))
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
    
if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]
    path = transformDirToInternal(path)
    h = libs.html.response.html()
    #h.write(path)
    page = fields.get("page",[None])[0]
    #h.write(str(page))
    thumbPerLine = int(fields.get("thumbPerLine", [5])[0])
    #h.write('calling album')
    if page is None:
        realPage = 0
    else:
        page = int(page)
        realPage = page
    l = tmpLog()
    i = collectionIterator.cachedPicIter(path, realPage, l)
    #h.write('after calling')
    h.genHead('Collections')
    showCollection(h, i, path, page)
    #h.write(l.s)
    h.genEnd()
