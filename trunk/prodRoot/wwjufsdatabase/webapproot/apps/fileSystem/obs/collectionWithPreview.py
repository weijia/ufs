import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *
import collectionV2

collectionExt=['jpg','jpeg','flv','avi','mp4','rm','rmvb']

def picIter(fullPath):
    l = os.listdir(fullPath)
    for i in l:
        if collectionV2.withExt(os.path.join(fullPath, i), collectionExt):
            p = os.path.join(fullPath, i).decode('gb2312').encode('utf8')
            yield [p,p]

def collectionWithPreview(htmlGen, fullPath):
    #htmlGen.write('<div style="white-space:nowrap">')
    htmlGen.write('<div style="max-width:40;float:right;max-height:100px;overflow-y:scroll;min-width:300px"><div id="log"></div></div>')
    htmlGen.write('<div id="collectionListContainer" style="max-height:100%%;float:left;overflow-y:scroll;min-width:200px;" border="1px">')
    htmlGen.write('<div id="collectionListInnerContainer">')
    i = picIter(fullPath)
    collectionV2.showCollection(htmlGen, i, 0, 1, nextPageUrl = "collectionWithPreview.py?path=%s&page="%fullPath.replace('\\','\\\\'))
    if True:
        h.write('''
            <script type="text/javascript">
                $(function() {
                    $("img").livequery(
                        function(){
                            $(this).lazyload({ 
                                failurelimit : 100,
                                effect : "fadeIn",
                                container:$("#collectionListContainer")
                            });
                        }
                    );
                    $("#previewImage").attr("width",$(window).width());
                    $("#collectionListContainer").scroll(function(){
                        //alert("scrolling");
                        //$("#log").text($("#log").text()+$("#collectionListContainer").scrollTop()+",");
                        //$("#log").text($("#log").text()+$("#collectionListInnerContainer").height()+",");
                        //$("#log").text($("#log").text()+$("#collectionListContainer").height()+"-");
                        if  ($("#collectionListContainer").scrollTop() == $("#collectionListInnerContainer").height() - $("#collectionListContainer").height()){
                            //alert("loading");
                            //$("#log").text($("#log").text()+"loading--");
                            //$("#log").text($("#log").text()+$("#collectionListContainer").scrollTop()+",");
                            //$("#log").text($("#log").text()+$("#collectionListInnerContainer").height()+",");
                            //$("#log").text($("#log").text()+$("#collectionListContainer").height()+"-");
                            lastPostFunc();
                        }
                    });
                });


                $(function() {
                        $(".thumbImage").livequery(
                            function(){
                                
                                //This following codes is an example for handling click on thumb
                                $(this).mouseover(function (){
                                        $(this).removeClass("clicked");
                                        //alert("callback");
                                        $("#previewImage").attr("src", $(this).attr("defaultTarget"));
                                    }
                                );
                            }
                        );
                    }
                );
            </script>
        ''')
    htmlGen.write('</div>')
    htmlGen.write('</div>')
    htmlGen.write('<div>')
    htmlGen.write('''
        <img id="previewImage" style="max-width:500px;"/>
    ''')
    htmlGen.write('</div>')

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]    
    page = int(fields.get("page",[0])[0])
    thumbPerLine = int(fields.get("thumbPerLine", [5])[0])
    #print 'calling album'
    #i = albumIterator(path)
    #print 'after calling'
    h = libs.html.response.html()
    h.genHead('Collections')
    h.write('<link rel="stylesheet" type="text/css" href="/webapproot/static/css/class.css" />')
    if page == 0:
        collectionWithPreview(h, path)
    else:
        i = picIter(path)
        collectionV2.showCollection(h, i, page, 1, nextPageUrl = "collectionWithPreview.py?path=%s&page="%path.replace('\\','\\\\'))
    h.genEnd()
