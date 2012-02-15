import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *
import collectionV4

import collectionIterator

def collectionWithPreview(htmlGen, fullPath, page):
    #htmlGen.write('<div style="white-space:nowrap">')
    h=htmlGen
    i = collectionIterator.cachedPicIter(fullPath, 0)
    h.write('<div style="float:left;min-width:25%">')
    collectionV4.showCollection(htmlGen, i, fullPath, page)
    h.write('</div>')
    if True:
        h.write('''
            <script type="text/javascript">
                $(function() {
                    $("img").livequery(
                        function(){
                            $(this).lazyload({ 
                                failurelimit : 100,
                                effect : "fadeIn",
                                container:$("#collectionList")
                            });
                        }
                    );

                    $(".thumbImage").livequery(
                        function(){
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
            </script>
        ''')
    htmlGen.write('<div style="white-space:nowrap">')
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
    collectionWithPreview(h, path, page)
    h.genEnd()
