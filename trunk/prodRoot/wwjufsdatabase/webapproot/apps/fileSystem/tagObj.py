import libSys
import libs.http.queryParam
import libs.html.response
import libs.tag.tagSystemInterface as tagSys
#from desktopApp.lib.transform import *
import libs.utils.transform as transform
import urllib
import libs.utils.configurationTools as configurationTools
import libs.utils.stringTools as stringTools
import libs.services.servicesV2 as service


def tagObj(req):
    fields = libs.http.queryParam.queryInfo().getAllFieldStorageUnicode()
    h = libs.html.response.html()
    h.genTxtHead()
    #fullPath = urllib.unquote(fields[u"path"][0])
    fullPath = fields[u"path"][0]
    fullPath = transform.transformDirToInternal(fullPath)
    #print fullPath
    #tags = urllib.unquote(fields[u"tags"][0])
    tags = fields[u"tags"][0]
    tl = stringTools.splitWithChars(tags, configurationTools.getTagSeparator())
    t = tagSys.getTagSysObj(req.getDbSys())
    t.tag(fullPath, tl)
    #h.write(u'{"path":"%s","tags":"%s"}'%(fullPath, (u','.join(tl))))
    
    h.write(u'{"path":"%s","tags":"%s"}'%(fullPath, (u','.join(t.getTags(fullPath)))))
    h.end()


if __name__=='__main__':
    tagObj(service.req())