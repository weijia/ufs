import libSys
import libs.tree.jsTreeNamedItemFuncV3 as jsTreeNamedItemFunc
import libs.html.response
import libs.ufs.ufsTreeItem as ufsTreeItem
import libs.ufs.winUfs as winUfs
try:
    from google.appengine.ext import webapp
except ImportError:
    import sys
    import os
    c = os.getcwd()
    while c.find('prodRoot') != -1:
      c = os.path.dirname(c)
    #print c
    sys.path.insert(0, os.path.join(c,'prodRoot'))
    import desktopApp.lib.localTreeItem as localTreeItem
    
gDebugFlag = False
    
def jsIdEncoding(s):
    '''
    This function is used to encode the item id of jstree as jstree can not manipulate id with ":" correctly
    '''
    l = s.split(u"_", 1)
    if len(l[0]) == 1:
        s = u":".join(l)
    return s


if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorageUnicode()
    path = fields.get("path", ["-1"])[0]
    path=jsIdEncoding(path)
    res = "Content-Type: text/html;charset=gbk\n\n"
    if gDebugFlag:
        h = libs.html.response.html()
        h.genHead('Collections')
    res += u'<!--'
    if path == "-1":
        p = winUfs.winUfsTreeItem()
    #res = path
    else:
        #p = desktopApp.lib.localTreeItem.localTreeItem(path.decode('utf8'))
        try:
            p = ufsTreeItem.getUfsTreeItem(path.decode('utf8'))
        except ValueError:
            #No schema/protocol string. Normal dir
            p = localTreeItem.localFolderTreeItem(path.decode('utf8'))
    data = jsTreeNamedItemFunc.containerList(p)
    res +=u'-->'
    #print res,d
    res += data
    if gDebugFlag:
        h.write(res)
        h.genEnd()
    else:
        print res.encode('gbk')

