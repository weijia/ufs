import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *
import collectionV3
import uuid
import libs.utils.misc
import shove
import libs.cache.collectionCache

collectionExt=['jpg','jpeg','flv','avi','mp4','rm','rmvb']
gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')


libs.utils.misc.ensureDir(gDbPath)
collectionPreviewPathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewPathDb.sqlite'))
collectionPreviewUuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewUuidDb.sqlite'))


def picIter(fullPath):
    for i in os.listdir(fullPath):
        if libs.utils.misc.withExt(os.path.join(fullPath, i), collectionExt):
            yield i.decode("gb2312")


def cachedPicIter(fullPath, page):
    imgPerLine = 1
    imgRowPerPage = 8
    fullPath = transformDirToInternal(fullPath)
    try:
        u = collectionPreviewPathDb[fullPath]
    except KeyError:
        u = str(uuid.uuid4())
        collectionPreviewPathDb[fullPath] = u
        collectionPreviewUuidDb[u] = fullPath
    start = page*imgRowPerPage*imgPerLine
    cnt = imgRowPerPage*imgPerLine
    iter = picIter(fullPath)
    ci = libs.cache.collectionCache.collectionCache(u)

    l = ci.listNamedChildrenPerRangeWithAutoRefresh(start, cnt, iter)
    for i in l:
        p = os.path.join(fullPath, i).encode('utf8')
        yield [p,p]
    


def collectionWithPreview(htmlGen, fullPath):
    #htmlGen.write('<div style="white-space:nowrap">')
    htmlGen.write('<div style="max-width:40;float:right;max-height:100px;overflow-y:scroll;min-width:300px"><div id="log"></div></div>')
    htmlGen.write('<div id="collectionListContainer" style="max-height:100%%;float:left;overflow-y:scroll;min-width:200px;" border="1px">')
    htmlGen.write('<div id="collectionListInnerContainer">')
    i = cachedPicIter(fullPath, 0)
    collectionV3.showCollection(htmlGen, i, 0,1, nextPageUrl = "collectionWithPreview.py?path=%s&page="%fullPath.replace('\\','\\\\'))
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

                    $(".thumbImage").livequery(
                        function(){
                            $(this).mouseover(function(){
                                    alert('in thumbImageLiveQuery');
                                    $("#previewImage").attr("src", "picList.py?path="+$(this).attr("path"));
                                }
                            );
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
        i = cachedPicIter(path, page)
        collectionV3.showCollection(h, i, page,1, nextPageUrl = "collectionWithPreview.py?path=%s&page="%path.replace('\\','\\\\'))
    h.genEnd()
