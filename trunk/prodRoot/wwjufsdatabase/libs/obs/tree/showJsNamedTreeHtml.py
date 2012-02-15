def genTreeInBody(sessionIns):
    response = sessionIns.getHtmlGen()
    extScriptList = ["/js/development-bundle/jquery-1.4.2.js","/js/jstree/jquery.jstree.js","/js/standalone/jquery.cookie.js"]
    #extScriptList = ["/js/jstree/jquery.jstree.js","/js/standalone/jquery.cookie.js"]
    #extScriptList = ["/js/jstree/jquery.tree.js","/js/jstree/plugins/jquery.tree.contextmenu.js"]
    response.inc(extScriptList)
    rootId = '3fe6382b-0219-40c7-add3-2f3b60aeb368'

    internalScript = '''
    function createNode(NODE, parentId) {
        var folderName = $(NODE.innerHTML).filter("a")[0].innerText;
        //var actionUrl = "/apps/utils/uuid.py";
        var actionUrl = "/apps/tree/addItemJasn.py?treeRoot="+parentId;
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
        var actionUrl = "/apps/tree/renameItem.py?itemId=" + itemId + "&itemNewName=" + itemNewName;
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
        var actionUrl = "/apps/tree/deleteItem.py?itemId=" + nodeId;
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
        $("#async_html_2").jstree({
            "plugins" : ["contextmenu", "cookies", "html_data", "themes"],
            "html_data" : { 
                "ajax" : {
                    "url" : function (n) {
                        if(n != -1) n = n.attr('id');
                        return "/apps/tree/jsTreeDbNamedItem.py?treeRoot=%s&dbName=%s&username="+username+"&id="+n;
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
            }

        }
        });
    });

    '''%(rootId,'treeImporterDb')
    response.script(internalScript)
    user = sessionIns.getUser()

    response.write('''
    <script type="text/javascript">
    var username = "%s";
    </script>
    <div>
        <div class="demo source" id="async_html_2">
        </div>
    </div>
    '''%user)
