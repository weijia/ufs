import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import desktopApp.lib.compress.zipClass as zipClass
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
        thumbFullPath = getThumb(fullPath, gWorkingDir)
        self.collectionInfoDict[itemObj.ufsUrl()] = infoDict
        #Add file to zip
        #return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
        return gDefaultInfoSize