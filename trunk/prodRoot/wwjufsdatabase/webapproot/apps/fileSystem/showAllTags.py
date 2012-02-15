import libSys
import libs.http.queryParam
import libs.html.response
import libs.tag.tagSystem
from desktopApp.lib.transform import *
import urllib


if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    h = libs.html.response.html()
    h.genTxtHead()
    t = libs.tag.tagSystem.tagSystemShoveDb()
    #print '{"path":"%s","tags":"%s"}'%(fullPath, ','.join(t.getTags(fullPath)))
    d = t.getTagDb()
    print d
    for i in d:
        print i, d[i]
    h.end()
