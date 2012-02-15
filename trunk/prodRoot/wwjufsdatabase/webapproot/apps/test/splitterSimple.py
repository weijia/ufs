import libs.services.services
s = libs.services.services.services()


import libs.tree.showJsNamedTreeHtml
h = s.getHtmlGen()
h.genHead('jQuery splitter demo')
h.write('<body>')
h.inc('/js/development-bundle/jquery-1.4.2.js')
h.inc('/js/splitter/splitter.js')

h.write('''
<style type="text/css" media="all">

html, body{
height:100%;width:100%; 
margin:0;padding:0;overflow: hidden;
}
#header{height:5%;}/* Header */

#splitterContainer {/* Main splitter element */
height:95%;width:100%;margin:0;padding:0;
}
#leftPane{
float:left;width:15%;height:100%;border-top:solid 1px #9cbdff;
overflow: auto;
}
#rightPane{	/*Contains toolbar and horizontal splitter*/
float:right;width:85%;height:100%;
}
#rightSplitterContainer{/*horizontal splitter*/	
width:100%;
} 

#rightTopPane{/*Top nested in horizontal splitter */
width:100%;height:50%;overflow:auto;
}
#rightBottomPane{/*Bottom nested in horizontal splitter */
width:100%;overflow:auto;
}


/* Splitbar styles; these are the default class names and required styles */
.splitbarV {
float:left;width:6px;height:100%;
line-height:0px;font-size:0px;
border-left:solid 1px #9cbdff;border-right:solid 1px #9cbdff;
background:#cbe1fb url(img/panev.gif) 0% 50%;
}
.splitbarH {
height:6px;text-align:left;line-height:0px;font-size:0px;
border-top:solid 1px #9cbdff;border-bottom:solid 1px #9cbdff;
background:#cbe1fb url(img/paneh.gif) 50% 0%;
}

.splitbuttonV{
margin-top:-41px;margin-left:-4px;top:50%;position:relative;
height:83px;width:10px;
background:transparent url(img/panevc.gif) 10px 50%;
}
.splitbuttonV.invert{
margin-left:0px;background:transparent url(img/panevc.gif) 0px 50%;
}
.splitbuttonH{
margin-left:-41px;left:50%;position:relative;
height:10px !important;width:83px;
background:transparent url(img/panehc.gif) 50% 0px;
}
.splitbuttonH.invert{
margin-top:-4px;background:transparent url(img/panehc.gif) 50% -10px;
}
.splitbarV.working,.splitbarH.working,.splitbuttonV.working,.splitbuttonH.working{
 -moz-opacity:.50; filter:alpha(opacity=50); opacity:.50;
}
</style>
<script type="text/javascript">

$(document).ready(function() {
$("#splitterContainer").splitter({minAsize:100,maxAsize:300,splitVertical:true,A:$('#leftPane'),B:$('#rightPane'),slave:$("#rightSplitterContainer"),closeableto:0});
$("#rightSplitterContainer").splitter({splitHorizontal:true,A:$('#rightTopPane'),B:$('#rightBottomPane'),closeableto:100});
});
</script>

<div id="header">
jQuery splitter demo- download all demo files <a href="splitter.zip">here</a></div>
<div id="splitterContainer">
	<div id="leftPane">''')
libs.tree.showJsNamedTreeHtml.genTreeInBody(s)

h.write('''

	</div>
	<!-- #leftPane -->
	<div id="rightPane">
	<div style="height:5%;background:#bac8dc">Toolbar?</div>
		<div id="rightSplitterContainer" style="height:95%">
			<div id="rightTopPane">
				<p>testing</p>
			</div>
			<!-- #rightTopPane-->
			<div id="rightBottomPane">
				<div>
					<p>some content</p>
				</div>
			</div>
			<!-- #rightBottomPane--></div>
		<!-- #rightSplitterContainer--></div>
	<!-- #rightPane --></div>
<!-- #splitterContainer -->


''')
h.write('</body>')
h.genEnd()
