




def genTreeInBody(response, addItemScript, renameItemScript, deleteItemScript, getChildrenScript, treeContainerId = 'treeContainer'):
    extScriptList = ["/webapproot/js/development-bundle/jquery-1.4.2.js","/webapproot/js/jstree/jquery.jstree.js","/webapproot/js/standalone/jquery.cookie.js"]
    response.inc(extScriptList)

    internalScript = '''
    function createNode(NODE, parentId) {
        var folderName = $(NODE.innerHTML).filter("a")[0].innerText;
        //var actionUrl = "/apps/utils/uuid.py";
        var actionUrl = "%s"+parentId;
        $.ajax(
            {
                type: "GET",
                url: actionUrl,
                data: null,
                dataType: "json",
                //dataType: "html",
                success: function(data) {
                    //alert(data.uuid);
                    NODE.id = data.uuid;
                    //alert(data);
                },
                error: function(req, status, error) {alert(error);
                }
            });
    }

    function renameNode(itemId, itemNewName) {
        var actionUrl = "%s" + itemId + "&itemNewName=" + itemNewName;
        $.ajax(
            {
                type: "POST",
                url: actionUrl,
                data: null,
                dataType: "json",
                success: function(data) {
                },
                error: function(req, status, error) {
                }
            });
    }
    function deleteSubNode(nodeId) {
        var actionUrl = "%s" + nodeId;
        $.ajax(
        {
            type: "POST",
            url: actionUrl,
            data: null,
            dataType: "json",
            success: function(data) {
            },
            error: function(req, status, error) {
            }
        });
    }

    $(document).ready(function() { 
        $("#%s").jstree({
            "plugins" : ["contextmenu", "cookies", "html_data", "themes"],
            "html_data" : { 
                "ajax" : {
                    "url" : function (n) {
                        if(n != -1) n = n.attr('id');
                        return "%s"+n;
                    }
                    // this function is executed in the instance's scope (this refers to the tree instance)
                    // the parameter is the node being loaded (may be -1, 0, or undefined when loading the root nodes)
                    /*
                    "data" : function (n) { 
                        // the result is fed to the AJAX request `data` option
                        return { 
                            "operation" : "get_children", 
                            "id" : n.attr ? n.attr("id").replace("node_","") : 1 
                        }; 
                    }*/
                }
            },
        "callback": {
           //oncreate: function(NODE, REF_NODE, TYPE, TREE_OBJ, RB) {alert("create");},
           //beforecreate: function(NODE, REF_NODE, TYPE, TREE_OBJ) {alert("before create");return true;},
           //onrename: function(NODE, TREE_OBJ, RB) {alert("onrename:"+TREE_OBJ.get_text(NODE));},
           
           //According to http://mohyuddin.blogspot.com/2009/08/persisting-jstree-changes-to-database.html
            oncreate: function(NODE, REF_NODE, TYPE, TREE_OBJ, RB) {
                var parent_id = 0;
                //alert(TREE_OBJ.parent($(REF_NODE)));
                //alert(TYPE);
                //alert($(REF_NODE).attr('id'));
                if (TYPE === "inside") {
                    parent_id = $(REF_NODE).attr('id');
                }
                if (TYPE == "after") {
                    parent_id = TREE_OBJ.parent($(REF_NODE)).attr('id');
                }
                createNode(NODE, parent_id);
            },

           /*
           */
           //onrename: function(NODE, TREE_OBJ, RB) {alert("onrename:"+TREE_OBJ.get_text(NODE));/*NODE.id="new created";*/}
            onrename: function(NODE, LANG, TREE_OBJ, RB) {
              //renameNode(NODE.id, $(NODE.innerHTML).filter("a")[0].innerText);
              //The following is got from http://hi.baidu.com/zhengaiai/blog/item/a925e422be97c4fbd6cae27e.html
              renameNode(NODE.id, $(NODE).find("a:first").text());
            },
            ondelete: function(NODE, TREE_OBJ, RB) {
                deleteSubNode(NODE.id);
            },
            onselect:function (NODE) {alert($(NODE).attr('id'));
            } 

        }
        });
    });

    '''%(addItemScript, renameItemScript, deleteItemScript, treeContainerId, getChildrenScript)
    response.script(internalScript)
    #response.write("<link rel="stylesheet" type="text/css" href="/webapproot/style.css" />")
    response.write('''
    <div>

        <div id="%s">
        </div>
    </div>
    '''%treeContainerId)




'''
class treeWidget:
    def __init__(self, t):
        self.treeElem = t
    def genTreeDiv(self):
        pass
'''
        
        
        
def main():
    pass
        
        
if __name__ == '__main__':
    main()