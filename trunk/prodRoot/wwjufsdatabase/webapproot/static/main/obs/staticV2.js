var collectionUrl = "../../apps/collection/jqueryListOnCollection.py";

var jstreeUrl = "../../apps/collection/jstreeOnCollectionV2.py?collectionId="
$(function() 
{
    /*
    $.ajaxSetup({
        'beforeSend' : function(xhr) {
            xhr.overrideMimeType('text/html; charset=UTF-8');
        },
    });
    */
  $(".bigIconButton").click(function(){$("#detailedView").attr("id", "bigIconView");});
  $(".detailButton").click(function(){$("#bigIconView").attr("id", "detailedView");});
  var curDir = $.cookie('lastLoadedPath');
  if(curDir == null)
  {
    //curDir = "C:/";//There is bug in jstree, so the first ":" is removed currently
    curDir = "C_0/";
  }
  $.cookie('curLoadPath', null);
  //Added cancel so quickTag class element can be clicked.
  //$("#existingList" ).selectable("cancel", '.quickTag');
  $("#existingList" ).selectable();
  //$(".connectedSortable" ).sortable({connectWith: ".connectedSortable"});
  $("#dirTreeInner").jstree({
    "plugins" : ["contextmenu", "cookies", "html_data", "themes","ui","sort","checkbox"],
    "html_data" : { 
        "ajax" : {
            "url" : function (n) {
                if(n != -1) n = n.attr('id');
                return jstreeUrl+n;
            }
        }
    }
  });
  //$(".thumbDiv").addClass("ui-widget-content");
  $("#dirTreeInner").bind("select_node.jstree", function(e, data) {
        //alert(data.rslt.obj.attr("id"));
        var path = data.rslt.obj.attr("id");
        if($.cookie('curLoadPath') == path) return;
        $.cookie('lastLoadedPath', path);
        $.cookie('curLoadPath', path);
        //alert("reloading when select tree item:"+path+"!="+$.cookie('curLoadPath'));
        $(".autoLoadPageOuterContainer").pageAutoLoad("reload", {"collectionId":path})
        /*
        $("li", "#existingList").remove();
        curDir = path.replace("\\","\\\\");
        //loadInitialDir(curDir);
        */
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
      $.get("../../apps/collection/collectionUpdater.py?jsonCollection=" + encoded,function(data){});
      console.log("send ok");
    });
  $.cookie('curLoadPath', curDir);
  $.cookie('lastLoadedPath', curDir);
  $(".autoLoadPageOuterContainer").pageAutoLoad({nextPageUrl:collectionUrl,nextPageParam:{"collectionId":curDir}});

  $(".thumbImage").livequery(function(){
      $(this).dblclick(function(){
            $.get("../../apps/fileSystem/execute.py?path=" + $(this).attr("path"),function(data){});
        }
      );
      
      $(this).lazyload({ 
          failurelimit : 100,
          effect : "fadeIn",
          container:$(".autoLoadPageOuterContainer"),
          placeholder : "../../static/images/waiting.gif"
      });
      
      //var p = unescape($(this).attr("path")).replace("\\","/");
      var p = $(this).attr("path").replace("\\","/");
      var s = p.lastIndexOf("/");
      var b = p.substr(s+1);
      var ta = $(".tagEditor", $(this).parents(".thumbDiv"));
      /*
      if(decodeURIComponent(b)!=b)
      {
        var t = decodeURIComponent(b) + "<-" + b;
      }
      else
      {
        var t = b;
      }
      */
      var naTxt = $("<p class=\"objDescriptionTxt\" title=\""+b+"\">"+b+"</p>");
      $(this).after(naTxt);
      
      ta.attr("contenteditable", "true");
      ta.editable({onEndEdit:function(elem){
              elem.addClass("submitting-tags");
              var p = $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
              //$.getJSON("../../apps/fileSystem/tagObj.py?path="+p+"&tags="+escape(elem.text()), function(data) {
              $.post("../../apps/fileSystem/tagObj.py",{"path":p,"tags=":elem.text()}, function(data) {
                  var d = $(".tagEditor", $("img[path="+data.path+"]").parent());
                  d.text(data.tags);
                  d.quickTagWidget("easyTag",d);
                  elem.removeClass("submitting-tags");
                  //alert(data.path);
              });
          }
      });
      
      /*
      ta.quickTagWidget({
        onAddTagCallback:function(elem, tag)
        {   
              var tagEditorElem = $(".tagEditor", elem.parents(".thumbDiv"));
              var p = $(".thumbImage", tagEditorElem.parents(".thumbDiv")).attr("path");
              $.getJSON("/wwjufsdatabase/webapproot/apps/fileSystem/tagObj.py?path="+p+"&tags="+tagEditorElem.text()+","+tag,
                  function(data) {
                      var d = $(".tagEditor", $("img[path="+data.path+"]").parent());
                      d.text(data.tags);
                      d.quickTagWidget("easyTag",d);
                      //elem.removeClass("submitting-tags");
                      //alert(data.path);
                  }
              );
        },
        
      });
      */
      ta.quickTagWidget({getElemUrlCallback:function(elem)
        {
            return $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
        }
      
      });
    }
  );
});