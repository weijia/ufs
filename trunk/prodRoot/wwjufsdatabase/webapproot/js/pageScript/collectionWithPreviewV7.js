$(function() {
    $(".thumbImage").livequery(
        function(){
            $(this).lazyload({ 
                failurelimit : 100,
                effect : "fadeIn",
                container:$("#collectionList"),
                placeholder : "/webapproot/static/images/waiting.gif"
            });

            var p = unescape($(this).attr("path")).replace("\\","/");
            var s = p.lastIndexOf("/");
            var b = p.substr(s+1);
            var t = unescape($(this).attr("tags")).replace("\\","/");
            if(t == "")
                t = "input tag";
            var ta = $("<div class=\"tagText\"><p>tag:</p><p class=\"tagEditor\" contenteditable=\"true\">"+t+"</p></div>");
            //ta.css({"margin-top":"-100px","margin-left":"120px"});
            var na = $("<div></div>");
            $(na[0]).addClass("objDescription");
            var naTxt = $("<p class=\"objDescriptionTxt\">"+b+"</p>");

            $(this).after(na);
            $(this).after(ta);
            $(this).after(naTxt);
            $(".tagEditor", ta).editable({onEndEdit:function(elem){
                    elem.css({"color":"red"});
                    var p = $(".thumbImage", elem.parents(".thumbDiv")).attr("path");
                    $.getJSON("tagObj.py?path="+p+"&tags="+elem.text(), function(data) {
                        var d = $(".tagEditor", $("img[path="+data.path+"]").parent());
                        d.text(data.tags);
                        d.css({"color":"black"});
                        alert(data.path);
                    });
                }
            });
            $(this).mouseover(function(){
                    //alert('in thumbImageLiveQuery');
                    $("#previewImage").attr("src", "picList.py?path="+$(this).attr("path"));
                }
            );
            $(this).dblclick(function(){
                    $.get("execute.py?path=" + $(this).attr("path"),function(data){});
                }
            );
        }
    );
    $("#previewImage").attr("width",$(window).width());
});
