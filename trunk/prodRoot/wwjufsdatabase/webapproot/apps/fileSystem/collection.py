import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *


gSupportedExt = ['jpg','avi']

def withExt(fullPath, extList = gSupportedExt):
    s = fullPath.split('.')
    if len(s) > 1:
        if  s[-1].lower() in extList:
            return True
    return False

def hasThumb(fullPath):
    return withExt(fullPath)
    
    
def albumIterator(fullDirPath):
    #print 'in iterator'
    allFiles = os.walk(fullDirPath)
    root = allFiles.next()
    if len(root[1]) > 1:
        #Has child directories
        for i in allFiles:
            p = os.path.join(fullDirPath,i[0])
            if not os.path.isdir(p):
                if hasThumb(p):
                    yield [p.decode('gb2312').encode('utf8'),p.decode('gb2312').encode('utf8')]
            else:
                for name in os.listdir(p):
                    if hasThumb(os.path.join(p, name)):
                        yield [p.decode('gb2312').encode('utf8'), os.path.join(p, name).decode('gb2312').encode('utf8')]
                        break
    
    else:
        #Dont have child directories, show files
        for i in root[2]:
            p = os.path.join(fullDirPath,i)
            if hasThumb(p):
                yield [p.decode('gb2312').encode('utf8'),p.decode('gb2312').encode('utf8')]

    
def showCollection(htmlGen, iter, page, thumbPerLine = 5, showPic = 'picList.py?path='):
    cnt = 0
    thumbViewScript = "picList.py?path="
    thumbViewScript = "http://localhost:8802/webapproot/apps/localServer/thumb.py?path="
    thumbViewScript = "http://localhost:8803/thumb?path="
    picListScript = "picList.py?path="
    picListScript = "collection.py?path="
    #thumbViewScript = "file:///"
    imgPerLine = thumbPerLine
    imgRowPerPage = 20
    h = htmlGen
    h.inc('/webapproot/js/development-bundle/jquery-1.4.2.js')
    h.inc('/webapproot/js/standalone/jquery.livequery.js')
    h.inc('/webapproot/js/standalone/jquery.lazyload.js')
    #print '<html><head>'
    h.write('<div class="wrdLatest" id=%d>'%page)
    #h.write("hello")
    #h.write("page:%d"%page)
    cnt = 0
    #h.write('before iter')
    for i, thumbPath in iter:
        #h.write('iterating')
        #h.write(i)
        if cnt >= page*imgRowPerPage*imgPerLine:
            if i != thumbPath:
                h.write('<a href="%s"><img src="%s%s" width="100px" height="100px"/></a>'%(picListScript+urllib.quote(i), thumbViewScript, urllib.quote(thumbPath)))
            else:
                h.write('<a href="%s"><img src="%s%s" width="100px" height="100px"/></a>'%(showPic+urllib.quote(i), thumbViewScript, urllib.quote(thumbPath)))
            if not ((cnt+1) % imgPerLine):
                h.write('<br>')
            cnt += 1
        #h.write(str(cnt))
        if cnt > page*imgRowPerPage*imgPerLine+imgRowPerPage*imgPerLine:
            break
    #h.write(str(fields))
    h.write("</div>")
    if page == 0:
        h.write('''
        <script type="text/javascript">
            function lastPostFunc() 
            { 
                //$('div#lastPostsLoader').html('<img src="bigLoader.gif">');
                $.get("collection.py?path=%s&page=" + (parseInt($(".wrdLatest:last").attr("id"))+1),     

                function(data){
                    if (data != "") {
                        $(".wrdLatest:last").after(data);            
                    }
                    //$('div#lastPostsLoader').empty();
                });
            }; 
            $(window).scroll(function(){
                if  ($(window).scrollTop() == $(document).height() - $(window).height()){
                   lastPostFunc();
                }
            });
            $(function() {
                $("img").livequery(
                    function(){$(this).lazyload({ 
                            failurelimit : 100,
                            effect : "fadeIn"
                        });
                    }
                );
            });
            </script>
        '''%path.replace('\\','\\\\'))

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]    
    page = int(fields.get("page",[0])[0])
    thumbPerLine = int(fields.get("thumbPerLine", [5])[0])
    #print 'calling album'
    i = albumIterator(path)
    #print 'after calling'
    h = libs.html.response.html()
    h.genHead('Collections')
    showCollection(h, i, page, thumbPerLine)
    #h.write('before gen end')
    h.genEnd()
