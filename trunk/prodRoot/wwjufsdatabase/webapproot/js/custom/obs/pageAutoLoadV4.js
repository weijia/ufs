var pageAutoLoad = {
  _init:function()
  {
    pageAutoLoad.loadInitialPage(this.options);
    //The following is a javascript clousure? The following callback will report var not find if use this.options
    var scrollOption = this.options;
    //this.element.css("overflow-y","scroll");//No effect if content is smaller than the container.
    this.element.scroll(function(){
        if($(scrollOption.outerContainer).scrollTop() >= $(scrollOption.innerContainer).height() - $(scrollOption.outerContainer).height())
        {
            /*
            //console.log("loading"+scrollOption.nextPageUrl);
            
            console.log($(scrollOption.outerContainer).scrollTop()+">="+$(scrollOption.innerContainer).height() + 
                "-" +$(scrollOption.outerContainer).height());
            */
            pageAutoLoad.loadInitialPage(scrollOption);
        }
    });
  },
  loadNewPageIfNeeded:function(){
    var scrollOption = this.options;
    if($(scrollOption.outerContainer).height()>$(scrollOption.innerContainer).height())
    {
      pageAutoLoad.loadInitialPage(scrollOption);
      return true;
    }
    return false;
  },
  reload:function(newParam, nextUrl){
    $(this.options.elementTag, this.options.innerContainer).remove();
    this.options.nextPageParam = newParam;
    this.options.nextPageUrl = nextUrl;
    pageAutoLoad.loadInitialPage(this.options);
  },
  loadInitialPage:function (options)
    {
      //alert(options.nextPageUrl);
      var calNextStart = 0;
      var lastElem = $(options.elementTag+":last", options.innerContainer);
      if(0 == lastElem.length)
      {
        //Create a hidden first element
        //alert("creating:"+options.elementTag);
        var newFirstElem = $("<"+options.elementTag+' style="display:none"/>');
        $(options.innerMostContainer, $(options.innerContainer)).append(newFirstElem);
        //alert($(options.innerMostContainer, $(options.innerContainer)).length);
        lastElem = $(options.elementTag+":last", options.innerContainer);
      }
      //alert(lastElem.length);
      //Check if a loading is going on
      if(lastElem.attr("loadingNew") != 1)
      {
          //alert(lastElem);
          lastElem.attr("loadingNew",1);
          if($(options.elementTag+":last", options.innerContainer).data("cnt") != undefined)
              calNextStart = $(options.elementTag+":last", options.innerContainer).data("cnt");
          //$.get(options.nextPageUrl+"&cnt="+options.pageCnt+"&start="+calNextStart, function (data)
          $.post(options.nextPageUrl,$.extend({}, options.nextPageParam, {"cnt":options.pageCnt,"start":calNextStart}), function (data)
          {
            //alert($(options.elementTag+":last", options.innerContainer).data("cnt"));
            var nextStart = options.pageCnt;
            if($(options.elementTag+":last", options.innerContainer).data("cnt") != undefined)
                nextStart += $(options.elementTag+":last", options.innerContainer).data("cnt");
                
            $(options.elementTag+":last", options.innerContainer).after(data);
            $(options.elementTag+":last", options.innerContainer).data("cnt", nextStart);
          });
      }
    },

  options: {
    //The outer container's selector, no enough space for the content. So it has scroll
    outerContainer:'.autoLoadPageOuterContainer',
    //The inner container's selector
    innerContainer:'.autoLoadPageInnerContainer',
    //The inner most container's selector, element will be created as this element's child
    innerMostContainer:'.autoLoadPageInnerMostContainer',
    //The request params will be posted from now on instead of set in get.
    //The following url will be passed with "&cnt="+pageCnt+"&start="+calNextStart
    nextPageUrl:"",
    //The above and following param will be submited
    nextPageParam:{},
    //Auto loading element's tag
    elementTag:"li",
    //Element in one page
    pageCnt:50
  }
};

$.widget("ui.pageAutoLoad", pageAutoLoad); // create the widget

