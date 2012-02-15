print "Content-Type: text/html;charset=utf-8"
print '''<html>
<head>
<title>
file tree
</title>
<script src="/js/jquery-1.4.2.min.js"></script>
<script>
  // Load jQuery
  //google.load("jquery", "1");
</script>
<script src="/js/jsTree/jquery.tree.js" type="text/javascript"></script>
<script type="text/javascript" src="/js/jsTree/jquery.tree.plugin.js"></script>
<script>

$(function () { 
	$("#async_html_2").tree({
		plugins : { 
			contextmenu : { }
		},
		data : { 
			async : true,
			opts : {
				url : "/apps/tree/jsTreeDb.py?treeRoot=%s&username=%s&dbName=%s"
			}
		}/*,
    callback: {
      beforedata: 
    }*/
	});
});

</script>
</head>
<body>
	<div class="demo source" id="async_html_2">
	</div>
</body>
</html>
'''%('3fe6382b-0219-40c7-add3-2f3b60aeb368','tester','treeImporterDb')