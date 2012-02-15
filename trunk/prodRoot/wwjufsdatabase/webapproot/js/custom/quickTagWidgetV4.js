var quickTagWidget = {
  easyTagTextClassName:"easyTagTexts",
  installQuickTagCallback:function(elem, curObj)
  {
    var options = curObj.options;
    //console.log(options);
    elem.mouseover(function(e){}).click(function(e)
        {
            //console.log(options);
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
            //e.cancelBubble();
            //The following should not be called before cancelBubble */
            //e.stopPropagation();
            return false;
        }
    );
  },
  submitTags:function(elem)
  {
    elem.addClass("submitting-tags");
    var p = $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
    var curObj = this;
    $.post(this.options.tagUrl,{"path":p,"tags":elem.text()}, function(data) {
        var d = $(".tagEditor", elem.parent());
        //console.log(d);
        data = $.parseJSON(data);
        d.text(data.tags);
        //console.log(d.text());
        curObj.easyTag(d, curObj);
        elem.removeClass("submitting-tags");
        elem.attr("contenteditable", "false");
        //alert(data.path);
    });
  },
  installNewTagCallback:function(elem, curObj)
  {
    var tagUrl = curObj.options.tagUrl;
    var options = curObj.options;
    var easyTag = curObj.easyTag;
    //var curObjToCallback = curObj;
    elem.click(function(e){
            ta = $(e.target);
            ta.attr("contenteditable", "true");
            ta.css("color","black");
            ta.editable({onEndEdit:function(elem){
                    elem.addClass("submitting-tags");
                    var p = $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
                    $.post(tagUrl,{"path":p,"tags":elem.text()}, function(data) {
                        var d = $(".tagEditor", elem.parent());
                        //console.log(d);
                        data = $.parseJSON(data);
                        d.text(data.tags);
                        //console.log(d.text());
                        easyTag(d, curObj);
                        curObj.installNewTagCallback($(".startToInputNewTag",curObj.element.parent()), curObj);
                        elem.removeClass("submitting-tags");
                        elem.attr("contenteditable", "false");
                        //alert(data.path);
                    });
                }
            });
            ta.editable("startEdit");
            //alert("startnew");
            //e.preventDefault();
            //The following exception is required.
            //Otherwise, selectable widget will continuously trigger the click event
            //e.cancelBubble();
            //The following should not be called before cancelBubble 
            //e.stopPropagation();
            return false;
    });
  },
  _init:function()
  {
    //console.log(this.options);
    this.easyTag(this.element, this);
    this.element.addClass(this.easyTagTextClassName);
    var tagUrl = this.options.tagUrl;
    //Add click event handler so tag can be easyly added
    this.installNewTagCallback($(".startToInputNewTag",this.element.parent()), this);
    //this.installQuickTagCallback($(".quickTag",this.element.parent()), this);
  },
  
  easyTag:function(element, curObj)
  {
    var tagList = element.text().split(',');
    var options = curObj.options;
    
    //console.log("currenttags:"+element.text());
    element.attr("currenttags", element.text());

    //Remove existing easy tag elements
    $(".quickTag",element.parent()).remove();
    $(".startToInputNewTag",element.parent()).remove();
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
    //var manualTags = "input other tags";
    var manualTags = "";
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
    predefinedTagElements += '<div class="startToInputNewTag">'+
            options.newTagText+' </div>';

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
    //Add a button for insert new tag
    element.before($(predefinedTagElements));
    curObj.installQuickTagCallback($(".quickTag",element.parent()), curObj);
  },
  options: {
    quickTags:['ºÃ'],
    //The following URL will be passed with param: path="+p+"&tags="+elem.text()
    tagUrl:"../../apps/fileSystem/appendTagForObj.py",
    removeTagUrl:"../../apps/fileSystem/removeTagForObj.py",    
    getElemUrlCallback:"",
    newTagText:"ÐÂ±êÇ©"
  }
};

$.widget("ui.quickTagWidget", quickTagWidget); // create the widget

