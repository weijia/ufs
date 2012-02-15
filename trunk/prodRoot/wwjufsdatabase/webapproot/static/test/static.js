var pageCnt = 50;

function loadInitialDir(path)
{
  //alert('loading');
  var calNextStart = 0;

  if($("li:last", "#existingList").data("cnt") != undefined)
      calNextStart = $("li:last", "#existingList").data("cnt");
  $.get("/webapproot/apps/localServer/collectionListItemsV3.py?path="+path+"&cnt="+pageCnt+"&start="+calNextStart, function (data)
  {
    //alert($("li:last", "#existingList").data("cnt"));
    var nextStart = pageCnt;
    if($("li:last", "#existingList").data("cnt") != undefined)
        nextStart += $("li:last", "#existingList").data("cnt");
        
    $("#existingList").append(data);
    $("li:last", "#existingList").data("cnt", nextStart);
  });
}

$(function() 
{
  var curDir = "c:/";
  $(".connectedSortable" ).sortable({connectWith: ".connectedSortable"});
  $("#dirTreeInner").jstree({
    "plugins" : ["contextmenu", "cookies", "html_data", "themes","ui","sort"],
    "html_data" : { 
        "ajax" : {
            "url" : function (n) {
                if(n != -1) n = n.attr('id');
                return "/webapproot/apps/localServer/getChildDirV2.py?path="+n;
            }
        }
    }
  });
  $("#dirTreeInner").bind("select_node.jstree", function(e, data) {
        //alert(data.rslt.obj.attr("id"));
        var path = data.rslt.obj.attr("id");
        $("li", "#existingList").remove();
        curDir = path.replace("\\","\\\\");
        loadInitialDir(curDir);
    });
  loadInitialDir(curDir);
  $(".collectionList").scroll(function(){
    if($(".collectionList").scrollTop() >= $(".collectionListInnerContainer").height() - $(".collectionList").height())
    {
        /*
        alert("loading"+curDir);
        
        alert($(".collectionList").scrollTop()+">="+$(".collectionListInnerContainer").height() + 
            "-" +$(".collectionList").height());
        */
        loadInitialDir(curDir)
    }

  });
  $(".thumbImage").livequery(function(){
      $(this).dblclick(function(){
            $.get("/webapproot/apps/localServer/execute.py?path=" + $(this).attr("path"),function(data){});
        }
      );
      /*
      $(this).lazyload({ 
          failurelimit : 100,
          effect : "fadeIn",
          container:$("#collectionList"),
          placeholder : "/webapproot/static/images/waiting.gif"
      });*/
      
      var p = unescape($(this).attr("path")).replace("\\","/");
      var p = $(this).attr("path").replace("\\","/");
      var s = p.lastIndexOf("/");
      var b = p.substr(s+1);
      var ta = $(".tagEditor", $(this).parents(".thumbDiv"));
      var limit = 15
      if(b.length > limit)
      {
        //trim the extra chars
        trimed = b.substring(0,limit - 4)+"...";
      }
      else
      {
        trimed = b;
      }
      var naTxt = $("<div class=\"objDescriptionTxt\" title=\""+b+"\">"+trimed+"</div>");

      $(this).after(naTxt);
      ta.attr("contenteditable", "true");
      ta.editable({onEndEdit:function(elem){
              elem.css({"color":"red"});
              var p = $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
              $.getJSON("/webapproot/apps/localServer/tagObj.py?path="+p+"&tags="+elem.text(), function(data) {
                  var d = $(".tagEditor", $("img[path="+data.path+"]").parent());
                  d.text(data.tags);
                  d.css({"color":"black"});
                  //alert(data.path);
              });
          }
      });
      

    }
  );
});