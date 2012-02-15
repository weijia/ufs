var pageAutoLoad = {
  _init:function()
  {
    this.loadInitialPage();
    var curObj = this;
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
            //console.log(curObj);
            curObj.loadInitialPage();
        }
    });
  },
  /*
  contentLessThanContainer:function ()
  {
    if($(this.options.outerContainer).height()>$(this.options.innerContainer).height())
    {
      if(this.options.extraData)
        return true;
    }
    return false;
  },*/
  loadNewPageIfNeeded:function(){
    var scrollOption = this.options;
    //console.log($(scrollOption.outerContainer).height()+","+$(scrollOption.innerContainer).height());
    if($(scrollOption.outerContainer).height()>$(scrollOption.innerContainer).height())
    {
      //console.log(this.options.extraData);
      if(this.options.extraData)
      {
        //Return true only there IS new data left. So the caller can know if additional call to this function are available.
        console.log("loading...");
        this.loadInitialPage();
        return true;
      }
    }
    return false;
  },
  reload:function(newParam, nextUrl){
    $(this.options.elementTag, this.options.innerContainer).remove();
    this.options.nextPageParam = newParam;
    this.options.nextPageUrl = nextUrl;
    this.options.extraData = true;
    this.loadInitialPage();
  },
  loadInitialPage:function ()
    {
      //alert(options.nextPageUrl);
      var options = this.options;
      var calNextStart = 0;
      var lastElem = $(options.elementTag+":last", options.innerContainer);
      if(0 == lastElem.length)
      {
        //Create a hidden first element
        //alert("creating:"+options.elementTag);
        var newFirstElem = $("<"+options.elementTag+' style="display:none" test="hello"/>');
        $(options.innerMostContainer, $(options.innerContainer)).append(newFirstElem);
        //alert($(options.innerMostContainer, $(options.innerContainer)).length);
        lastElem = $(options.elementTag+":last", options.innerContainer);
      }
      //alert(lastElem.length);
      //Check if a loading is going on
      if(lastElem.attr("loadingNew") != 1)
      {
          //alert(lastElem);
          //Used to prevent duplicated load request
          lastElem.attr("loadingNew",1);
          //The last element will contain a data("cnt"). It has the next start position of element need to be requested.
          if($(options.elementTag+":last", options.innerContainer).data("cnt") != undefined)
              calNextStart = $(options.elementTag+":last", options.innerContainer).data("cnt");
          //$.get(options.nextPageUrl+"&cnt="+options.pageCnt+"&start="+calNextStart, function (data)
          $.post(options.nextPageUrl,$.extend({}, options.nextPageParam, {"cnt":options.pageCnt,"start":calNextStart}), function (data)
          {
            //alert($(options.elementTag+":last", options.innerContainer).data("cnt"));
            var nextStart = options.pageCnt;
            if($(options.elementTag+":last", options.innerContainer).data("cnt") != undefined)
            {
                //New data arrival
                nextStart += $(options.elementTag+":last", options.innerContainer).data("cnt");
            }
            
            
            var jsonObj = $.parseJSON(data);
            genData = "";
            for(i=0; i<jsonObj.length; i++)
            {
                var curItem = jsonObj[i];
                genData += '<li class="thumbDiv ui-widget-content">';
                var tagStr = "";
                if(0 == curItem["tags"].length)
                {
                    tagStr = "input tag";
                }
                else
                {
                    tagStr = curItem["tags"].join(',');
                }
                
                var targetUrl = "http://localhost:8805/thumb?path=";
                genData += '<img class="thumbImage" src="http://localhost:8805/thumb?path='+curItem["utf8FullPath"]+'" path="'+curItem["fullPath"]+'"/>';
                genData += '<p class="tagEditor">'+ tagStr +'</p>';
                genData += '<div class="placeholder"></div></li>';
            }
            
            $(options.elementTag+":last", options.innerContainer).after(genData);
            //If last element already has data("cnt"), then no new data received, set the flag
            if($(options.elementTag+":last", options.innerContainer).data("cnt") != undefined)
            {
              console.log("no new data, set flag");
              options.extraData = false;
            }
            $(options.elementTag+":last", options.innerContainer).data("cnt", nextStart);
            options.newPageLoaded();
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
    pageCnt:40,
    //A flag indicate if there is still new data for the list
    extraData:true,
    //Callback for new content
    newPageLoaded:function(){}
  }
};

$.widget("ui.pageAutoLoad", pageAutoLoad); // create the widget

