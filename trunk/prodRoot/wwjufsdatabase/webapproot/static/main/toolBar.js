function initToolBar()
{
  //////////////////////////////////////////////////////////////
  //Buttons
  //////////////////////////////////////////////////////////////
  $("#iconButton").button();
  $("#recursiveButton").button();
  $("#iconButton").click(function(){
      if($("#iconButton").button( "option", "label" ) == "Big icon view")
      {
        $("#iconButton").button( "option", "label", "Detail view");
        $("#detailedView").attr("id", "bigIconView");
      }
      else
      {
        $("#iconButton").button( "option", "label", "Big icon view");
        $("#bigIconView").attr("id", "detailedView");
      }
    });
  $("#recursiveButton").click(function(){
        if($("#recursiveButton").button( "option", "label" ) == "Recursive view")
        {
            $("#recursiveButton").button( "option", "label", "Normal view");
            curCollectionUrl="../../apps/collection/jqueryListOnContainerCollection.py";
        }
        else
        {
            $("#recursiveButton").button( "option", "label", "Recursive view");
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
  $("#applyTags").button();
  $("#applyTags").click(function (){
    var applyingTags = $("#tagInput").attr("value");
    $("li.ui-selected .startToInputNewTag").text(applyingTags).each(function()
      {
        $(".easyTagTexts", $(this).parent()).quickTagWidget("submitTags",  $(this));
      }
    );
    $("li.ui-selected").removeClass("ui-selected")
    $( "input.selector" ).attr("checked",false);
  });
  
  $("#loginButton").usrLogin();
  
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
    $("#itemToolbar").css("top", pos.top+5).css("left",pos.left+100);
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

}