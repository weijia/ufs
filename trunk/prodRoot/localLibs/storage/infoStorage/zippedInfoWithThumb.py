import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import localLibs.compress.zipClass as zipClass
from zippedInfo import zippedInfo
from localLibs.thumb.thumbInterface import getThumb
import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *

gWorkingDir = "d:/tmp/working"
gDefaultInfoSize = 100

class zippedInfoWithThumb(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(zippedInfoWithThumb, self).__init__(workingDir)
        self.dbInst = objectDatabase.objectDatabase()
        
    def addItem(self, itemObj):
        infoDict = itemObj.getItemInfo()
        fullPath = itemObj["fullPath"]
        #Add thumb info
        thumbFullPath = getThumb(fullPath, gWorkingDir)
        if not (thumbFullPath is None):
            thumbObj = self.dbInst.getFsObjFromFullPath(thumbFullPath)
            thumbUfsUrl = thumbObj.getObjUfsUrl()
            infoDict["thumbnailFullPath"] = thumbFullPath
            infoDict["thumbnailUuid"] = thumbObj["uuid"]
            infoDict["thumbnailUrl"] = thumbUfsUrl
            infoDict["thumbnailHeadMd5"] = thumbObj.headMd5()
            self.collectionInfoDict[thumbUfsUrl] = thumbObj.getItemInfo()
        #Add item info
        self.collectionInfoDict[itemObj.getObjUfsUrl()] = infoDict
        ncl(infoDict)
        #Add file to zip
        thumbnailZippedSize = self.getZipFile().addfile(unicode(thumbFullPath), unicode(thumbFullPath))
        return gDefaultInfoSize*2 + thumbnailZippedSize.compress_size