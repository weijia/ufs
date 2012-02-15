import libSys
import libs.tree.treeWidgetV2
import libs.http.queryParam
import libs.html.response
import webapproot.apps.localServer.collectionWithPreviewV8 as collectionPreview

nextPageUrl = "collectionV8.py"


def showDirTree():
    #genTreeInBody(response, addItemScript, renameItemScript, deleteItemScript, getChildrenScript, treeContainerId = 'treeContainer'):
    libs.tree.treeWidgetV2.genTreeInBody(h, None, None, None, 'getChildDir.py?path=',treeContainerId = "dirTreeContainer")
    h.script('''$(function (){$("#%s").bind("select_node.jstree", function(e, data) {
        //alert(data.rslt.obj.attr("id"));
        var path = data.rslt.obj.attr("id");
        $("#collectionList").autoPager("reload", "%s?path="+path.replace("\\\\","\\\\\\\\")+"&page=");
    });});
    '''%("dirTreeContainer", nextPageUrl))


if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    #path = fields.get("path", ["-1"])[0]    
    h = libs.html.response.html()
    h.genHead('File manager')
    h.write('<div class="dirTree">')
    showDirTree()
    h.write('</div>')
    h.write('<div class="collectionList">')
    collectionPreview.collectionWithPreview(h, 'C:/',None)
    h.write('</div>')
    h.genEnd()
