var jstreeUrl = "../../apps/collection/jstreeOnCollectionV2.py?collectionId="
var curCollectionUrl="../../apps/collection/jqueryListOnContainerCollection.py"
var curCollectionUrl="../../apps/collection/jqueryListOnCollection.py"
var removeUrl="../../apps/fileSystem/removeItem.py"

function reset()
{
    $(".invisibleItem").show();
    $(".thumbDiv").removeClass("invisibleItem");
}


function filter(elems)
{
  reset();
  //console.log(elems);
  $(".thumbDiv").addClass("invisibleItem");
  elems.removeClass("invisibleItem");
  $(".invisibleItem").hide();
  //console.log("scroll-top is:"+$(".autoLoadPageOuterContainer").scrollTop());
  $( "#existingList" ).elementListWidget("loadNewPageIfNeeded");
}


$(function() 
{
  //////////////////////////////////////////////////////////////
  //Buttons
  //////////////////////////////////////////////////////////////
  $("#iconButton").button();
  $("#recursiveButton").button();
  $("#iconButton").click(function(){
      if($("#iconButton").button( "option", "label" ) == "Change to big icon view")
      {
        $("#iconButton").button( "option", "label", "Change to detail view");
        $("#detailedView").attr("id", "bigIconView");
      }
      else
      {
        $("#iconButton").button( "option", "label", "Change to big icon view");
        $("#bigIconView").attr("id", "detailedView");
      }
    });
  $("#recursiveButton").click(function(){
        if($("#recursiveButton").button( "option", "label" ) == "Change to recursive view")
        {
            $("#recursiveButton").button( "option", "label", "Change to normal view");
            curCollectionUrl="../../apps/collection/jqueryListOnContainerCollection.py";
        }
        else
        {
            $("#recursiveButton").button( "option", "label", "Change to recursive view");
            curCollectionUrl="../../apps/collection/jqueryListOnCollection.py";
        /*
        var path = $.cookie('curLoadPath');
        $("#curLoadedPath").text(path);
        $("#existingList").elementListWidget("reload", path, curCollectionUrl)
        */
        }
        var path = $.cookie('curLoadPath');
        $("#curLoadedPath").text(path);
        $("#existingList").elementListWidget("reload", path, curCollectionUrl)
    });
    
    
  $("#tagOperations").buttonset();
  
  $("#filterButton").click(function (){
    $(".thumbDiv").addClass("invisibleItem");
    //console.log($(".thumbDiv p[currenttags$='"+$("#tagSelector").attr("value")+"']").parent());
    //console.log($("#tagSelector").attr("value"));
    $(".thumbDiv p[currenttags*='"+$("#tagSelector").attr("value")+"']").each(function(){
      //console.log($(this).parent());
      $(this).parent().removeClass("invisibleItem");
    });
    //$(".thumbDiv:not(.visibleItem)").css({"display":"none"});
    $(".invisibleItem").hide();
  });
  $("#clearButton").click(function (){
    $(".invisibleItem").show();
    $(".thumbDiv").removeClass("invisibleItem");
  });
  
  $("#untaggedButton").click(function (){
    filter($(".thumbDiv p[currenttags='input tag']").parent());
  });

  $("#excactFilter").click(function(){
    filter($(".thumbDiv p[currenttags='"+$("#tagSelector").attr("value")+"']").parent());
  });
  //$("#applyTags").button();
  $("#applyTags").click(function (){
    var applyingTags = $("#tagInput").attr("value");
    $("li.ui-selected .startToInputNewTag").text(applyingTags).each(function()
      {
        $(".easyTagTexts", $(this).parent()).quickTagWidget("submitTags",  $(this));
      }
    );
  });

  //////////////////////////////////////////////////////////////
  //Tool bar
  //////////////////////////////////////////////////////////////
  
  $("#itemToolbar").hide().button();
  //console.log("before over");
  $(".thumbDiv").live("mouseover", function(event){
    var thD = $(event.target).parents(".thumbDiv");
    //console.log($(".thumbImage", thD).attr("path"));
    var pos = thD.position();
    if(pos == null) return;
    //console.log(pos);
    $("#itemToolbar").show().data("path", $(".thumbImage", thD).attr("path"));
    $("#itemToolbar").css("top", pos.top+20).css("left",pos.left+100);
  });
  //console.log("after over");
  $("#itemToolbar").click(function(){
    $.post(removeUrl,{"path":$("#itemToolbar").data("path")},function(data){
      data = $.parseJSON(data)
      //console.log(data);
      //console.log(data.path);
      //console.log($("[path='"+data.path+"']").parents(".thumbDiv"));
      $("[path='"+data.path+"']").parents(".thumbDiv").remove();
    });
  });
  
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
  $("#dirTreeInner").bind("select_node.jstree", function(e, data) {
        //alert(data.rslt.obj.attr("id"));
        var path = data.rslt.obj.attr("id");
        if($.cookie('curLoadPath') == path) return;
        $.cookie('lastLoadedPath', path);
        $.cookie('curLoadPath', path);
        //alert("reloading when select tree item:"+path+"!="+$.cookie('curLoadPath'));
        $("#curLoadedPath").text(path);
        console.log('loading:'+path);
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
      $.get("../../apps/collection/collectionUpdater.py?jsonCollection=" + encoded,function(data){});
      //console.log("send ok");
    });
  $.cookie('curLoadPath', curDir);
  $.cookie('lastLoadedPath', curDir);
  $("#curLoadedPath").text(curDir);
  
  //////////////////////////////////////////////////////////////
  //List
  //////////////////////////////////////////////////////////////
  $("#existingList" ).selectable();
  $("#existingList" ).elementListWidget(
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