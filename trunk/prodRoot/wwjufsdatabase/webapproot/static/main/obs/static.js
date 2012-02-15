/*
var pageCnt = 50;

function loadInitialDir(path)
{
  //alert('loading');
  $.cookie('lastLoadedPath', path);

  var calNextStart = 0;
  var lastElem = $("li:last", "#existingList");
  //Check if a loading is going on
  
  if(lastElem.attr("loadingNew") != 1)
  {
      lastElem.attr("loadingNew",1);
      if($("li:last", "#existingList").data("cnt") != undefined)
          calNextStart = $("li:last", "#existingList").data("cnt");
      $.get("/webapproot/apps/fileSystem/collectionListItemsV3.py?path="+path+"&cnt="+pageCnt+"&start="+calNextStart, function (data)
      {
        //alert($("li:last", "#existingList").data("cnt"));
        var nextStart = pageCnt;
        if($("li:last", "#existingList").data("cnt") != undefined)
            nextStart += $("li:last", "#existingList").data("cnt");
            
        $("#existingList").append(data);
        $("li:last", "#existingList").data("cnt", nextStart);
      });
  }
}
*/
$(function() 
{
  $(".bigIconButton").click(function(){$("#detailedView").attr("id", "bigIconView");});
  $(".detailButton").click(function(){$("#bigIconView").attr("id", "detailedView");});
  var curDir = $.cookie('lastLoadedPath');
  if(curDir == null)
  {
    //curDir = "C:/";//There is bug in jstree, so the first ":" is removed currently
    curDir = "C_/";
  }
  $.cookie('curLoadPath', null);
  $("#existingList" ).selectable();
  //$(".connectedSortable" ).sortable({connectWith: ".connectedSortable"});
  $("#dirTreeInner").jstree({
    "plugins" : ["contextmenu", "cookies", "html_data", "themes","ui","sort","checkbox"],
    "html_data" : { 
        "ajax" : {
            "url" : function (n) {
                if(n != -1) n = n.attr('id');
                return "/wwjufsdatabase/webapproot/apps/fileSystem/getChildDirV2.py?path="+n;
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
        $(".autoLoadPageOuterContainer").pageAutoLoad("reload", "/wwjufsdatabase/webapproot/apps/fileSystem/collectionListItemsV3.py?path="+path)
        /*
        $("li", "#existingList").remove();
        curDir = path.replace("\\","\\\\");
        //loadInitialDir(curDir);
        */
    });
  $.cookie('curLoadPath', curDir);
  $.cookie('lastLoadedPath', curDir);
  $(".autoLoadPageOuterContainer").pageAutoLoad({nextPageUrl:"/wwjufsdatabase/webapproot/apps/fileSystem/collectionListItemsV3.py?path="+curDir});
  //loadInitialDir(curDir);
  /*
  $(".collectionList").scroll(function(){
    if($(".collectionList").scrollTop() >= $(".collectionListInnerContainer").height() - $(".collectionList").height())
    {
        loadInitialDir(curDir)
    }

  });
  */
  $(".thumbImage").livequery(function(){
      $(this).dblclick(function(){
            $.get("/wwjufsdatabase/webapproot/apps/fileSystem/execute.py?path=" + $(this).attr("path"),function(data){});
        }
      );
      
      $(this).lazyload({ 
          failurelimit : 100,
          effect : "fadeIn",
          container:$(".autoLoadPageOuterContainer"),
          placeholder : "/wwjufsdatabase/webapproot/static/images/waiting.gif"
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
              $.getJSON("/wwjufsdatabase/webapproot/apps/fileSystem/tagObj.py?path="+p+"&tags="+elem.text(), function(data) {
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