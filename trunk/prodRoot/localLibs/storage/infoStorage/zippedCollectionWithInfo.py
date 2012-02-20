import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import wwjufsdatabase.libs.utils.fileTools as fileTools
import desktopApp.lib.compress.zipClass as zipClass

gWorkingDir = "d:/tmp"

class zippedCollectionWithInfo(object):
    def __init__(self):
        self.collectionInfoDict = {}
        self.zipFile = None
        self.zipFilePath = None
    def addItem(self, fullPath):
        #Get file info and add info to info dict
        fullPath = transform.transformDirToInternal(fullPath)
        itemObj = ufsObj.detailedFsObj(fullPath)
        self.collectionInfoDict[itemObj.ufsUrl()] = itemObj.getItemInfo()
        #Add file to zip
        self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
        #If size exceed certain value, generate a package and submit info to database
        pass
    def getZipFile(self):
        if self.zipFile is None:
            self.zipFilePath = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(gWorkingDir, '.zip'))
            self.zipFile = zipClass.ZFile(self.zipFilePath, 'w')
        return self.zipFile
    def finalizeZipFile(self):
        self.zipFile.close()
        self.zipFile = None
        return self.zipFilePath