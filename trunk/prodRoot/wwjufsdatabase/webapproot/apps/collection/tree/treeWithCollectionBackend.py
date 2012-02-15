import libSys
import libs.http.queryParam
import libs.html.response
import libs.tag.tagSystemV2 as tagSystem
from desktopApp.lib.transform import *
import urllib
import libs.utils.configurationTools as configurationTools
import libs.utils.stringTools as stringTools
import fileSystemCollection

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorageUnicode()
    h = libs.html.response.html()
    h.genJsonHead()
    fullPath = urllib.unquote(fields[u"path"][0])
    fullPath = transformDirToInternal(fullPath)
    
    
    for i in 
    h.end()
