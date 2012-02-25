import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import wwjufsdatabase.libs.utils.fileTools as fileTools
import desktopApp.lib.compress.zipClass as zipClass

gWorkingDir = "d:/tmp"

class zippedCollectionWithInfo(object):
    def __init__(self, workingDir = gWorkingDir):
        self.collectionInfoDict = {}
        self.zipFile = None
        self.zipFilePath = None
        self.workingDir = workingDir
    def addItem(self, fullPath):
        #Get file info and add info to info dict
        fullPath = transform.transformDirToInternal(fullPath)
        itemObj = ufsObj.detailedFsObj(fullPath)
        self.collectionInfoDict[itemObj.ufsUrl()] = itemObj.getItemInfo()
        #Add file to zip
        return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))

    def getZipFile(self):
        if self.zipFile is None:
            self.zipFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.workingDir, '.zip'))
            self.zipFile = zipClass.ZFile(self.zipFilePath, 'w')
        return self.zipFile
    def finalizeZipFile(self):
        self.zipFile.close()
        self.zipFile = None
        return self.zipFilePath