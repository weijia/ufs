import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *
import collectionV6

import collectionIteratorV2
import os
from desktopApp.lib.transform import *

#import shove
import libs.cache.encryptedShove as shove
import uuid


gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

def fileIter(fullPath):
    for i in os.listdir(fullPath):
        try:
            p = os.path.join(fullPath, i)
            if not os.path.isdir(p):
                yield i.decode("gb2312")
        except UnicodeDecodeError:
            continue


libs.utils.misc.ensureDir(gDbPath)
collectionPreviewPathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewPathDb.sqlite'))
collectionPreviewUuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewUuidDb.sqlite'))

def collectionWithPreview(htmlGen, fullPath, page):
    #htmlGen.write('<div style="white-space:nowrap">')
    h=htmlGen
    try:
        u = collectionPreviewPathDb[fullPath]
    except KeyError:
        u = str(uuid.uuid4())
        collectionPreviewPathDb[fullPath] = u
        collectionPreviewUuidDb[u] = fullPath
    iter = fileIter(fullPath)
    i = collectionIteratorV2.cachedCollectionIter(u, iter, 0)
    h.write('<div style="float:left;min-width:25%">')
    co = []
    for k in i:
        p = os.path.join(fullPath, k)
        co.append([p, p])
    #h.write(str(co))

    collectionV6.showCollection(htmlGen, co, fullPath, None)
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
                            var p = unescape($(this).attr("path")).replace("\\\\","/");
                            var s = p.lastIndexOf("/");
                            var b = p.substr(s+1);
                            var na = $("<div><p>"+b+"</p></div>");
                            na.css({"color":"white","background":"black",
                                "opacity":0.3,"margin-top":"-40px","height":"40px","font-size":"16",
                                "padding-left":"10px","padding-top":"10px"});
                            
                            $(this).after(na);
                            
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
