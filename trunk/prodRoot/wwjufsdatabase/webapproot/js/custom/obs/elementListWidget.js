var elementListWidget = {
    options: {
        //tagUrl: "../../apps/fileSystem/tagObj.py",
        //tagUrl: "../../apps/fileSystem/appendTagForObj.py",
        executeUrl:"../../apps/fileSystem/execute.py",
        //executeParam:{},
        outerContainerSelector:".autoLoadPageOuterContainer",
        curLoadPathForList:"D:/tmp",
        collectionUrl:"../../apps/collection/jqueryListOnContainerCollection.py"
    },

    _init:function()
    {
        //Create an enclosure so this option can be used in the functions embeded in this function
        var options = this.options;
        $(options.outerContainerSelector).pageAutoLoad({nextPageUrl:options.collectionUrl,nextPageParam:{"collectionId":options.curLoadPathForList}});
        $(".thumbImage").livequery(function(){
            $(this).dblclick(function(){
                $.post(options.executeUrl,{"path":$(this).attr("path")},function(data){});
                }
            );
      
            $(this).lazyload({ 
              failurelimit : 10,
              effect : "fadeIn",
              container:$(options.outerContainerSelector),
              placeholder : "../../static/images/waiting.gif"
            });

            var p = $(this).attr("path").replace("\\","/");
            var s = p.lastIndexOf("/");
            var b = p.substr(s+1);
            var ta = $(".tagEditor", $(this).parents(".thumbDiv"));

            var naTxt = $("<p class=\"objDescriptionTxt\" title=\""+p+"\">"+b+"</p>");
            $(this).after(naTxt);

            ta.quickTagWidget({getElemUrlCallback:function(elem)
                {
                    return $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
                }
            });
        });
    },
    reset:function()
    {
        $(".invisibleItem").show();
        $(".thumbDiv").removeClass("invisibleItem");
    },
    filter:function(tag)
    {
      this.reset();
      //console.log(elems);
      $(".thumbDiv").addClass("invisibleItem");
      elems.removeClass("invisibleItem");
      $(".invisibleItem").hide();
      //console.log("scroll-top is:"+$(".autoLoadPageOuterContainer").scrollTop());
      $("."+this.options.outerContainerSelector).pageAutoLoad("loadNewPageIfNeeded", function(){this.filter(tag)});
    },
    reload:function(path, collectionUrl)
    {
        $(this.options.outerContainerSelector).pageAutoLoad("reload", {"collectionId":path}, collectionUrl);
    }


}

$.widget("ui.elementListWidget", elementListWidget); // create the widget
