import libSys
import desktopApp.lib.localTreeItem
import libs.tree.jsTreeNamedItemFunc
import libs.html.response

gDebugFlag = False

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields.get("path", ["-1"])[0]
    res = "Content-Type: text/html;charset=utf-8\n\n"
    if gDebugFlag:
        h = libs.html.response.html()
        h.genHead('Collections')
    res += '<!--'
    if path == "-1":
        p = desktopApp.lib.localTreeItem.localWindowsRootItem()
    #res = path
    else:
        p = desktopApp.lib.localTreeItem.localTreeItem(path.decode('utf8'))
    data = libs.tree.jsTreeNamedItemFunc.dirlist(p)
    res +='-->'
    #print res,d
    res += data
    if gDebugFlag:
        h.write(res)
        h.genEnd()
    else:
        print res

