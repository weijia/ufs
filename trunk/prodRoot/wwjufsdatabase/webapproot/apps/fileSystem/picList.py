import libSys
import libs.html.response
import libs.platform.services
import os
import urllib

import libs.thumb.picThumbGenerator

def show_file(path):
    import serve_file
    files = serve_file.file_request_handler()
    #newPath = libs.thumb.picThumbGenerator.genPicThumb(path, "d:/tmp/")
    #thumbFile = libs.thumb.picThumbGenerator.returnThumbString(path)
    #files.serveStringFile(thumbFile, path)
    files.serve(path)

  
def show_dir():
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]
    if not os.path.isdir(path):
        show_file(path)
    else:
        thumbViewScript = "picList.py?path="
        thumbViewScript = "http://localhost:8802/webapproot/apps/localServer/thumb.py?path="
        thumbViewScript = "http://localhost:8803/thumb?path="
        #thumbViewScript = "file:///"
        imgPerLine = 5
        imgRowPerPage = 20
        page = int(fields.get("page",[0])[0])
        h = libs.html.response.html()
        h.genHead('hello world')
        h.inc('/webapproot/js/development-bundle/jquery-1.4.2.js')
        h.inc('/webapproot/js/standalone/jquery.lazyload.js')
        #print '<html><head>'
        h.write('<div class="wrdLatest" id=%d>'%page)
        #h.write("hello")
        #h.write("page:%d"%page)
        cnt = 0
        for name in os.listdir(path):
            if cnt > page*imgRowPerPage*imgPerLine:
                try:
                    h.write('<img src="%s%s" width="100px" height="100px"/>'%(thumbViewScript, os.path.join(path, name.decode('gb2312'))))
                except:
                    pass
                if not (cnt % imgPerLine):
                    h.write('<br>')
            cnt += 1
            if cnt > page*imgRowPerPage*imgPerLine+imgRowPerPage*imgPerLine:
                break
        h.write(str(fields))
        h.write("</div>")
        if page == 0:
            h.write('''
            <script type="text/javascript">
                function lastPostFunc() 
                { 
                    //$('div#lastPostsLoader').html('<img src="bigLoader.gif">');
                    $.get("picList.py?path=%s&page=" + (parseInt($(".wrdLatest:last").attr("id"))+1),     

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
                    $("img").lazyload({ 
                        failurelimit : 100,
                        effect : "fadeIn"
                    });
                });
                </script>
            '''%path.replace('\\','\\\\'))
        h.genEnd()

if __name__=='__main__':
    show_dir()