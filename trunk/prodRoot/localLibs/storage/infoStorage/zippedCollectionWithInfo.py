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
        self.additionalInfoDict = {}
        self.zipFile = None
        self.zipFilePath = None
        self.workingDir = workingDir
    def addAdditionalInfo(self, addInfo):
        for i in addInfo:
            self.additionalInfoDict[i] = addInfo[i]
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
        #Add info to zip file
        self.additionalInfoDict["collectionContentInfo"] = self.collectionInfoDict
        s = json.dumps(self.additionalInfoDict, sort_keys=True, indent=4)
        infoFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.workingDir, '.log', 'zippedCollFile'))
        logFile = open(infoFilePath, 'w')
        logFile.write(s)
        logFile.close()
        self.zipFile.addfile(unicode(infoFilePath), unicode(infoFilePath))
        self.zipFile.close()
        #Set attribute so new zip will be created if this object is still in use
        self.zipFile = None
        return self.zipFilePath