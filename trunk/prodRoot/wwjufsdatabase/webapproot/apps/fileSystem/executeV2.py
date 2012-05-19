import os
import urllib

import libSys
import libs.http.queryParam
import libs.html.response
import libs.tag.tagSystemInterface as tagSys
#from desktopApp.lib.transform import *
import libs.utils.transform as transform

import libs.utils.configurationTools as configurationTools
import libs.utils.stringTools as stringTools
import libs.services.servicesV2 as service
import libs.utils.objTools as objTools

import localLibSys
import localLibs.services.launcherService as launcherService

def startAppOrOpenFile(fullPath):
    try:
        ext = os.path.splitext(fullPath)[1]
    except:
        ext = ''
    if (ext in ['.bat', '.py']):
        launcherService.launcherService().launch([fullPath])
        #raise "stop here"
        return "app"
    else:
        os.startfile('"'+fullPath+'"')
        #raise "stop there"
        return "doc"

def executeAppOrOpenFile(req):
    fields = libs.http.queryParam.queryInfo().getAllFieldStorageUnicode()
    h = libs.html.response.html()
    h.genTxtHead()
    #fullPath = urllib.unquote(fields[u"path"][0])
    fullPath = fields[u"path"][0]
    if objTools.isUfsFs(fullPath):
        fullPath = objTools.getFullPathFromUfsUrl(fullPath)
    fullPath = transform.transformDirToInternal(fullPath)
    #print fullPath
    #tags = urllib.unquote(fields[u"tags"][0])
    tags = "sys.executable"
    tl = stringTools.splitWithChars(tags, configurationTools.getTagSeparator())
    t = tagSys.getTagSysObj(req.getDbSys())
    #t.tag(fullPath, tl)
    #h.write(u'{"path":"%s","tags":"%s"}'%(fullPath, (u','.join(tl))))
    res = startAppOrOpenFile(fullPath)
    if res == "app":
        t.tag(fullPath, tl)

    h.write(u'{"path":"%s","tags":"%s"}'%(fullPath, (u','.join(t.getTags(fullPath)))))
    h.end()

if __name__=='__main__':
    executeAppOrOpenFile(service.req())