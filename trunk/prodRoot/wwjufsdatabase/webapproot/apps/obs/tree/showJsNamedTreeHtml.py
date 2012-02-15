import libs.html.response

def genTree(h):
    h.inc(["/js/jquery-1.4.2.min.js","/js/jsTree/jquery.tree.js","/js/jsTree/plugins/jquery.tree.contextmenu.js"])

    h.addScript('''

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
        var actionUrl = "/apps/tree/renameItem?itemId=" + itemId + "&itemNewName=" + itemNewName;
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

    $(function () { 
      $("#async_html_2").tree({
          plugins : { 
          contextmenu : { }
        },
        data : { 
          async : true,
          opts : {
            url : "/apps/tree/jsTreeDbNamedItem.py?treeRoot=%s&username=%s&dbName=%s"
          }
        },
        callback: {
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

    '''%('3fe6382b-0219-40c7-add3-2f3b60aeb368','tester','treeImporterDb'))
    h.genHead('file tree', extScriptList, internalScript)
    print '''
    <body>
      <div class="demo source" id="async_html_2">
      </div>
    </body>
    '''
    h.genEnd()