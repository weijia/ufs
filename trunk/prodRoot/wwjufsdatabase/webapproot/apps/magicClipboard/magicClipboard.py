print "Content-Type: text/html;charset=utf-8"
print '''<html>
<head>
<title>magic clipboard
</title>
<script src="/js/jquery-1.4.2.min.js"></script>
<script>
  // Load jQuery
  //google.load("jquery", "1");
</script>
<script src="/js/jqueryFileTree/jqueryFileTree.js"></script>
<script src="/js/jqueryFileTree/jquery.easing.1.3.js" type="text/javascript"></script>
<link href="/js/jqueryFileTree/jqueryFileTree.css" rel="stylesheet" type="text/css" media="screen" />
<script>

$(document).ready( function() {
  
  $('#container_id').fileTree({ root: '/%s/', script: '/apps/tree/jqueryDbTree.py?username=%s&dbName=%s' }, function(file) { 
    alert(file);
  });
  
});
</script>
</head>
<body>

  <div id = "container_id" style="display:inline-block"></div>
  <div style="display:inline;">
    <textarea rows="10" cols="10"></textarea>
  </div>
  <div>
    <textarea rows="10" cols="10" name="inputText">input</textarea>
    <textarea rows="10" cols="10" name="outputText">output</textarea>
    <input class="output" type="submit" value="transform"/>
  </div>
</body>
</html>
'''%('3fe6382b-0219-40c7-add3-2f3b60aeb368','tester','treeImporterDb')
