import libSys
import libs.tree.treeWidgetV2
import libs.http.queryParam
import libs.html.response
import webapproot.apps.localServer.collectionWithPreviewV5

def showDirTree():
    #genTreeInBody(response, addItemScript, renameItemScript, deleteItemScript, getChildrenScript, treeContainerId = 'treeContainer'):
    libs.tree.treeWidgetV2.genTreeInBody(h, None, None, None, 'getChildDir.py?path=',treeContainerId = "dirTreeContainer")
    h.script('''$(function (){$("#%s").bind("select_node.jstree", function(e, data) {
        //alert(data.rslt.obj.attr("id"));
        var path = data.rslt.obj.attr("id");
        $("#collectionList").autoPager("reload", "collectionV6.py?path="+path.replace("\\\\","\\\\\\\\")+"&page=");
    });});
    '''%"dirTreeContainer")


if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    #path = fields.get("path", ["-1"])[0]    
    h = libs.html.response.html()
    h.genHead('File manager')
    h.write('<div style="float:left;max-width:30%;max-height:100%;overflow-x:auto;min-height:100%;min-width:25%">')
    showDirTree()
    h.write('</div>')
    h.write('<div style="white-space:nowrap;max-height:100%;min-width:70%;overflow-x:auto;min-height:100%">')
    webapproot.apps.localServer.collectionWithPreviewV5.collectionWithPreview(h, 'C:/',None)
    h.write('</div>')
    h.genEnd()
