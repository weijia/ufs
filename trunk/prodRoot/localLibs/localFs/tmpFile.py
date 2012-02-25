import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
from localLibs.logSys.logSys import *
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import os

def getStorgePathWithDateFolder(rootPath, ext = ".enc"):
    gTimeV = time.gmtime()
    yearStr = time.strftime("%Y", gTimeV)
    monthStr = time.strftime("%m", gTimeV)
    dayStr = time.strftime("%d", gTimeV)
    dateTimeDir = yearStr+"/"+monthStr+"/"+dayStr
    newEncDir = unicode(os.path.join(rootPath, dateTimeDir))
    misc.ensureDir(newEncDir)
    targetPath = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(newEncDir, ext))
    return targetPath

