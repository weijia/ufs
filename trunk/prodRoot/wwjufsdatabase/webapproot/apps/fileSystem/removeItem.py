import libSys
import libs.http.queryParam
import libs.html.response
import libs.tag.inheritableExclusableTagSystem as tagSystem
#from desktopApp.lib.transform import *
import urllib
import libs.utils.configurationTools as configurationTools
#import libs.utils.stringTools as stringTools
import shutil
import os
import uuid
import localLibSys
import localLibs.cache.localFileSystemCache as localFileSystemCache
import libs.ufsDb.dbSys as dbSys

import libs.utils.misc as misc
import libs.utils.transform as transform



if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorageUnicode()
    h = libs.html.response.html()
    h.genTxtHead()
    dbSysInst = dbSys.dbSysSmart()
    fullPath = urllib.unquote(fields[u"path"][0])
    fullPath = transform.transformDirToInternal(fullPath)
    
    rootPath = configurationTools.getRootDir()
    recyclePath = os.path.join(rootPath, 'recycle')
    misc.ensureDir(recyclePath)

    dst = os.path.join(recyclePath, str(uuid.uuid4())+os.path.basename(fullPath))
    localFileSystemCache.localFileSystemCache(dbSysInst).moveCached(fullPath, dst)
    #print fullPath
    h.write(u'{"path":"%s","removed":"true"}'%fullPath)
    h.end()
