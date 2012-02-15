var jstreeUrl = "../../apps/collection/jstreeOnCollectionV2.py?collectionId="
var curCollectionUrl="../../apps/collection/jqueryListOnContainerCollection.py"
var curCollectionUrl="../../apps/collection/jqueryListOnCollection.py"
var removeUrl="../../apps/fileSystem/removeItem.py"


$(function() 
{
  $('body').layout({ applyDefaultStyles: true });
  initToolBar();
    //////////////////////////////////////////////////////////////
  //Tree
  //////////////////////////////////////////////////////////////
  var curDir = $.cookie('lastLoadedPath');
  if(curDir == null)
  {
    //curDir = "C:/";//There is bug in jstree, so the first ":" is removed currently
    curDir = "C_0/";
  }
  $.cookie('curLoadPath', null);

  $("#dirTreeInner").jstree({
    "plugins" : ["contextmenu", "cookies", "html_data", "themes","ui","checkbox"],
    "html_data" : { 
        "ajax" : {
            "url" : function (n) {
                if(n != -1) n = n.attr('id');
                return jstreeUrl+encodeURI(n);
            },
            "type":"POST",
        }
    }
  });
  $("#dirTreeInner").bind("select_node.jstree", function(e, data) {
        //alert(data.rslt.obj.attr("id"));
        var path = data.rslt.obj.attr("id");
        if($.cookie('curLoadPath') == path) return;
        $.cookie('lastLoadedPath', path);
        $.cookie('curLoadPath', path);
        //alert("reloading when select tree item:"+path+"!="+$.cookie('curLoadPath'));
        $("#curLoadedPath").text(path);
        //console.log('loading:'+path);
        $("#clearButton").trigger("click");
        $("#existingList").elementListWidget("reload", path, curCollectionUrl)
        
    });
    $("#dirTreeInner").bind("change_state.jstree", function(e, data){
      var se = new Array();
      //var cnt = 0;
      $("#dirTreeInner").jstree("get_checked").each(function(index){
        se.push($(this).attr("id"));
        //cnt += 1;
      });
      var op = {"update":{"uuid://3b84d155-cc5c-428e-8009-12d5fdc68b2a":se}};
      var encoded = $.toJSON(op)
      $.get("../../apps/collection/collectionUpdaterV2.py?jsonCollection=" + encoded,function(data){});
      //console.log("send ok");
    });
  $.cookie('curLoadPath', curDir);
  $.cookie('lastLoadedPath', curDir);
  $("#curLoadedPath").text(curDir);

  
  //////////////////////////////////////////////////////////////
  //List
  //////////////////////////////////////////////////////////////
  $( "#existingList" ).selectable("cancel", 'image,div');
  $( "#existingList" ).elementListWidget(
    {
      curLoadPathForList:curDir,
      collectionUrl:curCollectionUrl,
      newContentLoaded:function()
      {
        //This function will be called when new content is loaded. So if filtering are functionning, it will filter the new content
        $( "#tagOperations :checked" ).trigger("click");
      }
  });

  
});