$(function() 
{
  $(".bigIconButton").click(function(){$("#detailedView").attr("id", "bigIconView");});
  $(".detailButton").click(function(){$("#bigIconView").attr("id", "detailedView");});
  var curDir = $.cookie('lastLoadedPathForList');
  if(curDir == null)
  {
    curDir = "D_0/tmp";
  }

  $("#existingList" ).elementListWidget({curLoadPathForList:curDir});
});