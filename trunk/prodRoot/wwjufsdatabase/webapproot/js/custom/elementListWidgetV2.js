var elementListWidget = {
    options: {
        //tagUrl: "../../apps/fileSystem/tagObj.py",
        //tagUrl: "../../apps/fileSystem/appendTagForObj.py",
        executeUrl:"../../apps/fileSystem/executeV2.py",
        //executeParam:{},
        outerContainerSelector:".autoLoadPageOuterContainer",
        curLoadPathForList:"D:/tmp",
        collectionUrl:"../../apps/collection/jqueryListOnContainerCollection.py",
        newContentLoaded:function(){}
        /*
        filtering:false,
        reloadNew:true
        */
    },
    /*
    newContentLoadedCallback:function()
    {
      if(this.options.filtering&&this.options.reloadNew)
      {
        
      }
    },*/
    _init:function()
    {
        //Create an enclosure so this option can be used in the functions embeded in this function
        var options = this.options;
        $(options.outerContainerSelector).pageAutoLoad({nextPageUrl:options.collectionUrl,nextPageParam:{"collectionId":options.curLoadPathForList},newPageLoaded:options.newContentLoaded});
        $( "li.thumbDiv" ).live("click", function(e){
            $(this).toggleClass("ui-selected");
            $( ".selector" ,$(this)).attr("checked", $(this).hasClass("ui-selected"));
        }).live("dblclick",function(e){
            $(this).addClass("ui-selected");
            $( ".selector" , $(this)).attr("checked", true);
            $.post(options.executeUrl,{"path":$( ".thumbImage" , $(this)).attr("path")},function(data){});
            return false;
        });
        //$( "input.selector" ).live("check")
        $(".thumbImage").livequery(function(){
            $(this).before('<input class="selector" type="checkbox"/>');
            /*
            $(this).dblclick(function(){
                    $( ".selector" , $(this).parent()).attr("checked", true);
                    $(this).parent().addClass("ui-selected");
                    
                    $.post(options.executeUrl,{"path":$(this).attr("path")},function(data){});
                    return false;
                }
            )*/
      
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

            var naTxt = $('<p class=\"objDescriptionTxt\" title=\"'+p+"\">"+b+'</p>');
            $(this).after(naTxt);

            ta.quickTagWidget({getElemUrlCallback:function(elem)
                {
                    return $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
                }
            });
        });
    },
    /*
    reset:function()
    {
        $(".invisibleItem").show();
        $(".thumbDiv").removeClass("invisibleItem");
    },
    filter:function(tag)
    {
      this.options.filteringTag = tag;
      self.filterInternal();
    },
    filterInternal:function()
    {
      this.reset();
      var filteringTag = this.options.filteringTag;
      //console.log(elems);
      $(".thumbDiv").addClass("invisibleItem");
      elems.removeClass("invisibleItem");
      $(".invisibleItem").hide();
      //console.log("scroll-top is:"+$(".autoLoadPageOuterContainer").scrollTop());
      if($("."+this.options.outerContainerSelector).pageAutoLoad("contentLessThanContainer"))
      {
        //Need to load new content
        $("."+this.options.outerContainerSelector).pageAutoLoad("loadInitialPage", this.filterInternal);
      }
    },
    
    showAll:function()
    {
        $(".thumbDiv").show();
    },
    showOnlyClass:function(classNameToShow)
    {
        $(".invisibleItem").show();
        $(".thumbDiv").addClass("invisibleItem");
        $("."+classNameToShow).removeClass("invisibleItem");
        $(".invisibleItem").hide();
        if($(this.options.outerContainerSelector).pageAutoLoad("loadNewPageIfNeeded"))
          this.options.
    },*/
    loadNewPageIfNeeded:function()
    {
      return $(this.options.outerContainerSelector).pageAutoLoad("loadNewPageIfNeeded");
    },
    reload:function(path, collectionUrl)
    {
        $(this.options.outerContainerSelector).pageAutoLoad("reload", {"collectionId":path}, collectionUrl,this.options.newContentLoaded);
    }


}

$.widget("ui.elementListWidget", elementListWidget); // create the widget
