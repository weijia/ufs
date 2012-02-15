var autoPager = {
  
  //structure:
  //  container: user specified container/window, size don't change, will has autoPagerNextUrl
  //    inner container: with size increase with auto load
  //      page container: every page has one page container
  
  pageContainerClassName:"autoPagerPageContainer",
  innerContainerClassName:"autoPagerInnerContainer",
  userContainerClassName:"autoPagerUserContainer",
  loadFirstPage: function()
  {
    var lastElem = $("."+autoPager.pageContainerClassName+":last");
    $.get(lastElem.parents("."+autoPager.userContainerClassName).filter(':first').data("autoPagerNextUrl") + "0",
        function(data){
            if (data != "") {
                var lastElem = $("."+autoPager.pageContainerClassName+":last");
                var newData = $(data).wrapAll('<div/>');
                newData.data("pageNum",0);
                newData.addClass(autoPager.pageContainerClassName);
                lastElem.after(newData);
                //alert(newData.data("pageNum"));
            }
            //$('div#lastPostsLoader').empty();
        }
    );

  },

  _init:function()
  {
    this.element.addClass(this.userContainerClassName);
    var userContainer = this.element;
    var innerContainer = userContainer.wrapInner('<div class="'+this.innerContainerClassName+'"/>').children("."+this.innerContainerClassName);
    //alert(innerContainer.attr("class"));
    var pageContainer = innerContainer.wrapInner('<div class="'+this.pageContainerClassName+'"/>').children("."+this.pageContainerClassName);
    //alert(pageContainer.attr("class"));
    pageContainer.data("pageNum", 0);
    userContainer.data("autoPagerNextUrl", this.options.nextPageUrl);
    
    function lastPostFunc() 
    { 
        //$('div#lastPostsLoader').html('<img src="bigLoader.gif">');
        var lastElem = $("."+autoPager.pageContainerClassName+":last");
        if(lastElem.attr("loadingNew") != 1)
        {
            lastElem.attr("loadingNew",1);
            //alert(lastElem.parents("."+autoPager.userContainerClassName).filter(':first').attr("class"));
            $.get(lastElem.parents("."+autoPager.userContainerClassName).filter(':first').data("autoPagerNextUrl") + (lastElem.data("pageNum")+1),
                function(data){
                    if (data != "") {
                        var lastElem = $("."+autoPager.pageContainerClassName+":last");
                        lastElem.removeAttr("loadingNew");
                        var newData = $(data).wrapAll('<div/>');
                        newData.data("pageNum",lastElem.data("pageNum")+1);
                        newData.addClass(autoPager.pageContainerClassName);
                        lastElem.after(newData);
                        //alert(newData.data("pageNum"));
                    }
                    //$('div#lastPostsLoader').empty();
                }
            );
        }
    };


    userContainer.scroll(function(){
        //alert(innerContainer.attr("class"));
        //$("#log").text($("#log").text()+userContainer.scrollTop()+"==");
        //$("#log").text($("#log").text()+innerContainer.height()+"-");
        //$("#log").text($("#log").text()+userContainer.height()+"?");
        if  (userContainer.scrollTop() >= innerContainer.height() - userContainer.height()){
            //alert("loading");
            //$("#log").text($("#log").text()+"loading--");
            //$("#log").text($("#log").text()+$("#collectionListContainer").scrollTop()+",");
            //$("#log").text($("#log").text()+$("#collectionListInnerContainer").height()+",");
            //$("#log").text($("#log").text()+$("#collectionListContainer").height()+"-");
            lastPostFunc();
        }
    });
    if(this.options.autoLoadFirst)
    {
        autoPager.loadFirstPage();
    }
  },
  reload:function (nextUrl){
    //Remove existing items
    $("."+autoPager.pageContainerClassName).remove();

    var pageContainer = $("."+autoPager.innerContainerClassName).wrapInner('<div class="'+this.pageContainerClassName+'"/>').children("."+this.pageContainerClassName);
    pageContainer.data("pageNum", 0);
    var userContainer = $("."+autoPager.userContainerClassName);
    userContainer.data("autoPagerNextUrl", nextUrl);
    //Load the first page
    autoPager.loadFirstPage();
  },
  options: {
    nextPageUrl:'',
    autoLoadFirst:false
  }
};

$.widget("ui.autoPager", autoPager); // create the widget
/*Usage:
$("#collectionList").autoPager({nextPageUrl:"next.py"});
*/
