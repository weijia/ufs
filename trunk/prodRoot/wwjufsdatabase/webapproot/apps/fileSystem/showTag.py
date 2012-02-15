import libSys
import libs.http.queryParam
import libs.html.response
import libs.tag.tagSystemV2 as tagSystem
from desktopApp.lib.transform import *
import urllib


if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    h = libs.html.response.html()
    h.genTxtHead()
    fullPath = urllib.unquote(fields["path"][0])
    fullPath = transformDirToInternal(fullPath)
    #print fullPath
    t = tagSystem.tagSystemShoveDb()
    print '{"path":"%s","tags":"%s"}'%(fullPath, ','.join(t.getTags(fullPath)))
    h.end()
