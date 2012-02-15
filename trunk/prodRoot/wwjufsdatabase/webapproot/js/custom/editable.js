var editable = {
  _init:function()
  {
    function createCallback(onEndEditCallback)
    {
        var callback = onEndEditCallback;
        var res = function(e){
            //alert("onblur");
            if($(e.target).data("originalTag") != $(e.target).text())
            {
                callback($(e.target));
            }
        }
        return res
    }
    //this.element.attr("contenteditable", "true");
    this.element.blur(createCallback(this.options.onEndEdit)/*function(e){
            //alert("onblur");
            if($(e.target).data("originalTag") != $(e.target).text())
            {
                this.options.onEndEdit($(e.target));
            }
        }*/
    ).keypress(function(e){
            //alert(e.keyCode);
            if(e.keyCode == 13) {
                //alert('Enter key was pressed.');
                //return false;
                //e.keyCode = 9;
                //return false;
            }
        }
    ).keydown(function(e) {
            //alert(e.keyCode);
            if(e.keyCode == 13) {
                //alert('Enter key was pressed.');
                //return false;
                //e.keyCode = 9;
                $(this).get(0).blur();
                return false;
            }
        }
    ).focus(function (e){
            window.setTimeout(function(){
                window.getSelection().setBaseAndExtent(
                    e.target, 0, e.target, e.target.childNodes.length
                );
                $(e.target).data("originalTag", $(e.target).text());
            });
        }
    );
  },
  startEdit:function()
  {
    this.element.focus();
  },
  options: {
    onEndEdit:''
  }
};

$.widget("ui.editable", editable); // create the widget

