var usrLogin = {
  _init:function()
  {
    var setPrimaryUserUrl = this.options.setPrimaryUserUrl;
    function arrangeUserList(allUser)
    {
        var allUserList;
        if(allUser==null) allUserList = new Array();
        else allUserList = allUser.split('\n');
        console.log(allUserList);
        var exist = false;
        var seen = {};
        var resList = new Array();
        //Remove duplicated items
        for(i in allUserList)
        {
            if(seen[allUserList[i]]) continue;
            seen[allUserList[i]] = true;
            console.log(allUserList[i]);
            resList.push(allUserList[i]);
        }
        allUser = resList.join('\n');
        return allUser;
        $.cookie('allUser', allUser);
    }
    
    function verifyPassCallback(data)
    {
        //console.log(d);
        data = $.parseJSON(data);
        if(data.state != "OK")
        {
            $( "#dialog-form" ).updateTips("Wrong passwd");
        }
        else
        {
            //console.log(curUser);
            var curUser = data.username;
            $.cookie('curUser', curUser);
            //Update user list
            var secondaryUsers = data.secondaryUsers;
            secondaryUserList = secondaryUsers.split(',');
            var allUser = secondaryUserList.join("\n");
            allUser = arrangeUserList(allUser)
            $.cookie('allUser', allUser);
            //console.log(curUser);
            $("#loginButton").button("option", "label", curUser);
            //console.log($("#loginButton").button( "option", "label"));
            $( "#dialog-form" ).dialog( "close" );
        }
    }

    $(this.element).button().click(function() {
              $( ".menuDiv" ).remove();
              $( "#dialog-form" ).dialog( "open" );
            });
    var menuRootElement = $(this.element);
    $(this.element).button().mouseover(function(e){
        var allUser = $.cookie('allUser');
        allUser = arrangeUserList(allUser)
        var menuList = allUser.split('\n');
        var menuDiv = $('<div class="menuDiv"></div>');
        var menuUl = $("<ul></ul>");
        for(i=0;i<menuList.length;i++)
        {
          if(menuList[i] == "")
            continue;
          //var domInput = $(this).get(0).inputField;
          menuItem = $("<li>"+menuList[i]+"</li>");//.css({"margin":2,"padding":2,"color":"black"});
          menuItem.css({"list-style-type":"none"});
          //menuItem.get(0).inputField = domInput;
          menuItem.mouseover(
            function ()
            {
              //$(this).css({"background":"blue"});
              $(this).addClass( "ui-state-hover" );
            }
          );
          menuItem.mouseout(
            function ()
            {
              //$(this).css({"background":"white"});
              $(this).removeClass( "ui-state-hover" );
            }
          );
          menuItem.click(
            function ()
            {
              //alert("menu clicked");
              if(curMenuDiv != null)
              {
                curMenuDiv.remove();
                curMenuDiv = null;
              }
              var curUser = $(this).text();
              //$.cookie('curUser', curUser);
              //$("#loginButton").button("option", "label", curUser);
              $( ".menuDiv" ).remove();
              $.post(setPrimaryUserUrl,{"username":curUser}, verifyPassCallback)

            }
          );
          menuUl.append(menuItem);
        }
        menuDiv.append(menuUl);
        var iconPos = menuRootElement.offset();
        //menuUl.css({"margin":2,"padding":2});
        menuDiv.addClass( "ui-widget" );
        //menuUl.addClass( "ui-button" );
        //console.log(iconPos);
        //console.log(menuRootElement.height());
        menuDiv.css({'position':'absolute','top':iconPos.top+menuRootElement.height(),'left':iconPos.left-menuDiv.width(),"z-index":999,"background":"white"/*, "border-radius":"3px","border": "solid 1px black"*/});
        curMenuDiv = menuDiv;
        $("body").append(menuDiv);
        //menuDiv.mouseout(function(){menuDiv.remove();});
    });
    var curUsr = $.cookie('curUser');
    var loginUrl = this.options.loginUrl;
    if(curUsr != null)
    {//If user already login
      $(this.element).button( "option", "label", curUsr);
    }
    var name = $( "#name" ),
      //email = $( "#email" ),
      password = $( "#password" ),
      allFields = $( [] ).add( name ).add( password ),//.add( email ),
      tips = $( ".validateTips" );
    function updateTips( t ) {
      tips
        .text( t )
        .addClass( "ui-state-highlight" ).addClass( ".ui-widget" );
      setTimeout(function() {
        tips.removeClass( "ui-state-highlight", 1500 );
      }, 500 );
    }

    function checkLength( o, n, min, max ) {
      if ( o.val().length > max || o.val().length < min ) {
        o.addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " +
          min + " and " + max + "." );
        return false;
      } else {
        return true;
      }
    }

    function checkRegexp( o, regexp, n ) {
      if ( !( regexp.test( o.val() ) ) ) {
        o.addClass( "ui-state-error" );
        updateTips( n );
        return false;
      } else {
        return true;
      }
    }
    $( "#dialog-form" ).dialog({
      autoOpen: false,
      height: 320,
      width: 370,
      modal: true,
      buttons: {
        "Login": function() {
          var bValid = true;
          allFields.removeClass( "ui-state-error" );

          bValid = bValid && checkLength( name, "username", 3, 16 );
          //bValid = bValid && checkLength( email, "email", 6, 80 );
          bValid = bValid && checkLength( password, "password", 2, 16 );

          bValid = bValid && checkRegexp( name, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
          // From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
          //bValid = bValid && checkRegexp( email, /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i, "eg. ui@jquery.com" );
          bValid = bValid && checkRegexp( password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );

          if ( bValid ) {
                curUser = name.val();
                $.post(loginUrl,{"username":curUser,"passwd":password.val()}, verifyPassCallback)
              /*
              //console.log(curUser);
              $.cookie('curUser', curUser);
              //console.log(curUser);
              $("#loginButton").button("option", "label", curUser);
              //console.log($("#loginButton").button( "option", "label"));
            $( this ).dialog( "close" );
            */
          }
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      },
      close: function() {
        allFields.val( "" ).removeClass( "ui-state-error" );
      }
      });
  },
  options: {
    loginUrl:"../../apps/user/simpleUserLoginV2.py",
    setPrimaryUserUrl:"../../apps/user/switchPrimaryUser.py",
  }
};

$.widget("ui.usrLogin", usrLogin); // create the widget

