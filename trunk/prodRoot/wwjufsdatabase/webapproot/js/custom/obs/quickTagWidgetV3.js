var quickTagWidget = {
  easyTagTextClassName:"easyTagTexts",
  _init:function()
  {
    quickTagWidget.easyTag(this.element);
    this.element.addClass(quickTagWidget.easyTagTextClassName);
    var tagUrl = this.options.tagUrl;
    //Add click event handler so tag can be easyly added
    var options = this.options;
    $(".quickTag",this.element.parent()).mouseover(function(e){
        
    }).click(function(e)
        {
            var elem = $(e.target);
            var nextClass = "";
            var nextUrl = "";
            //alert($(e.target).text());
            if($(e.target).hasClass("quickTag-tagged"))
            {
                //Remove the tag
                $(e.target).removeClass("quickTag-tagged");
                $(e.target).addClass("quickTag-changing");
                nextClass = "quickTag-untagged";
                nextUrl = options.removeTagUrl;
            }
            else
            {
                //Add the tag
                $(e.target).removeClass("quickTag-untagged");
                $(e.target).addClass("quickTag-changing");
                nextClass = "quickTag-tagged";
                nextUrl = options.tagUrl;
            }
            var p = options.getElemUrlCallback(elem);
            $.post(nextUrl,{"path":p,"tags":elem.text()}, function(data) {
                data = $.parseJSON(data);
                //$.getJSON(nextUrl+"path="+p+"&tags="+elem.text(), function(data) {
                elem.removeClass("quickTag-changing");
                elem.addClass(nextClass);
                //alert(data.path);
            });
            //e.preventDefault();
            //The following exception is required.
            //Otherwise, selectable widget will continuously trigger the click event
            e.cancelBubble();
            //The following should not be called before cancelBubble */
            //e.stopPropagation();
            return false;
        }
    );

  },
  
  easyTag:function(element)
  {
    var tagList = element.text().split(',');
    var options = this.options;
    
    console.log("currenttags:"+element.text());
    element.attr("currenttags", element.text());

    //Remove existing easy tag elements
    $(".quickTag",element.parent()).remove();
    
    /*
    //Currently, all tags are made easy tag buttons
    //Remove tags in input field
    var lastTagList = new Array();
    for(j=0;j<tagList.length;j++)
    {
        console.log('checking:'+tagList[j]);
        if(jQuery.inArray(tagList[j], options.quickTags)==-1)
        {
            //The tag on the element is not a common tag, add it to the final list
            lastTagList.push(tagList[j]);
            console.log('adding:'+tagList[j]+','+options.quickTags.join(','));
        }
    }
    */
    var manualTags = "input other tags";
    element.text(manualTags);
    
    //Add quick tag buttons, tags already applied will also been added here
    //First add existing non-common tags
    var newEasyTags = $.merge([], options.quickTags);
    //Must remove duplicated elements when concat
    //options.quickTags.concat(tagList);
    for(j=0;j<tagList.length;j++)
    {
        //console.log('checking:'+tagList[j]);
        if(jQuery.inArray(tagList[j], options.quickTags)==-1)
        {
            //The tag on the element is not a common tag, add it to the final list
            newEasyTags.push(tagList[j]);
            //console.log('adding:'+tagList[j]+','+options.quickTags.join(','));
        }
    }

    //console.log("easy tags:"+tagList.join(",")+","+options.quickTags.join(","));
    var predefinedTagElements = "";
    for(i=0;i<newEasyTags.length; i++)
    {
        //Remove the input tag text before the collectionList script was updated
        if(newEasyTags[i] == "input tag")
            continue;
        //Create the easy tag button
        if(jQuery.inArray(newEasyTags[i], tagList)!=-1)
        {
            //Tag is already applied
            tagClass = "quickTag quickTag-tagged";
        }
        else
        {
            //Tag is not applied to this element
            tagClass = "quickTag quickTag-untagged";
        }
        predefinedTagElements +='<div class="'+tagClass+'" tagContent="'+newEasyTags[i]+'"> '+
            newEasyTags[i]+' </div>';
    }
    element.before($(predefinedTagElements));
    
  },
  options: {
    quickTags:['��'],
    //The following URL will be passed with param: path="+p+"&tags="+elem.text()
    tagUrl:"../../apps/fileSystem/appendTagForObj.py",
    removeTagUrl:"../../apps/fileSystem/removeTagForObj.py",    
    getElemUrlCallback:"",
  }
};

$.widget("ui.quickTagWidget", quickTagWidget); // create the widget

