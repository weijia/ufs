import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import localLibs.compress.zipClass as zipClass
from zippedInfo import zippedInfo
from localLibs.thumb.thumbInterface import getThumb

gWorkingDir = "d:/tmp/working"
gDefaultInfoSize = 100

class zippedCollectionWithInfo(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(zippedCollectionWithInfo, self).__init__(workingDir)
    def addItem(self, fullPath):
        itemObj = self.getItemFromFullPath(fullPath)
        infoDict = itemObj.getItemInfo()
        #Add thumb info
        thumbFullPath = getThumb(fullPath, gWorkingDir)
        if not (thumbFullPath is None):
            thumbObj = self.getItemFromFullPath(thumbFullPath)
            thumbUfsUrl = thumbObj.ufsUrl()
            infoDict["thumbnailFullPath"] = thumbFullPath
            infoDict["thumbnailUuid"] = thumbObj["uuid"]
            infoDict["thumbnailUrl"] = thumbUfsUrl
            infoDict["thumbnailHeadMd5"] = thumbObj.headMd5()
        self.collectionInfoDict[thumbUfsUrl] = thumbObj.getItemInfo()
        #Add item info
        self.collectionInfoDict[itemObj.ufsUrl()] = infoDict
        #Add file to zip
        thumbnailZippedSize = self.getZipFile().addfile(unicode(thumbFullPath), unicode(thumbFullPath))
        return gDefaultInfoSize*2 + thumbnailZippedSize