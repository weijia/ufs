import libSys
import libs.tree.treeWidget
import libs.http.queryParam
import libs.html.response

def showDirTree():
    #genTreeInBody(response, addItemScript, renameItemScript, deleteItemScript, getChildrenScript, treeContainerId = 'treeContainer'):
    libs.tree.treeWidget.genTreeInBody(h, None, None, None, 'getChildDir.py?path=')


if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    #path = fields.get("path", ["-1"])[0]    
    h = libs.html.response.html()
    h.genHead('Dir tree')
    h.write('<div style="max-width:30%;max-height:100%;overflow-x:auto;min-height:100%">')
    showDirTree()
    h.write('</div>')
    h.genEnd()
