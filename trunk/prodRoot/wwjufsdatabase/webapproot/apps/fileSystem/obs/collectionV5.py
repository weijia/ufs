import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *

import collectionIterator


class webWidgetBase:
    def getExtScripts(self):
        '''
        Return a list of external script this widget will use
        '''
        pass

    def getDocReadyScript(self):
        '''
        Return a script that will be executed after document is loaded. No <script> tag needed
        '''
        pass
    def getPageContent(self):
        '''
        Return the content for the page
        '''
        pass

        
class thumbCollectionWidget(webWidgetBase):
    def __init__(self):
        self.collectionWidgetName = 'collectionList'
    def getExtScripts(self):
        res = []
        res.append('/webapproot/js/development-bundle/jquery-1.4.2.js')
        res.append('/webapproot/js/development-bundle/ui/jquery-ui-1.8.2.custom.js')
        res.append('/webapproot/js/standalone/jquery.livequery.js')
        res.append('/webapproot/js/standalone/jquery.lazyload.js')
        res.append('/webapproot/js/custom/pageAutoLoad.js')
        return res
    def getDocReadyScript(self):
        return '''
        $(".%s").autoPager({nextPageUrl:"%s",autoLoadFirst:true});
        '''%(self.collectionWidgetName, 'collectionV5.py')
    def getPageContent(self):
        '''
        Return the content for the page
        '''
        res = []
        res.append('<link rel="stylesheet" type="text/css" href="/webapproot/static/css/class.css" />')
        res.append('<div id="collectionList" style="max-height:100%;overflow-y:scroll;">')

        
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

    
def showCollectionPerPage(h, i, page, path):
    h.write('<div>')
    h.write(showThumbCollection(i))
    #h.write('before gen end')
    h.write('</div>')

    
if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]
    path = transformDirToInternal(path)
    page = int(fields.get("page",[0])[0])
    thumbPerLine = int(fields.get("thumbPerLine", [5])[0])
    #print 'calling album'
    i = collectionIterator.cachedPicIter(path, page)
    #print 'after calling'
    h = libs.html.response.html()
    h.genHead('Collections')
    showCollection(h, i, page, path)
    h.genEnd()
