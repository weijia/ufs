import re
import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import wwjufsdatabase.libs.utils.fileTools as fileTools
import localLibs.compress.zipClass as zipClass
from localLibs.logSys.logSys import *

gWorkingDir = "d:/tmp"
gDefaultInfoSize = 100
gInfoFilePrefix = 'zippedCollFile'
gInfoFileExt = "log"

class zippedInfo(object):
    def __init__(self, workingDir = gWorkingDir):
        self.collectionInfoDict = {}
        self.additionalInfoDict = {}
        self.package_file = None
        self.package_file_full_path = None
        self.workingDir = workingDir
    def addAdditionalInfo(self, addInfo):
        for i in addInfo:
            self.additionalInfoDict[i] = addInfo[i]
            
    def addItem(self, itemObj):
        self.collectionInfoDict[itemObj.ufsUrl()] = itemObj.getItemInfo()
        #Add file to zip
        #return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
        return gDefaultInfoSize


    def finalizeZipFile(self):
        #Add info to zip file
        self.additionalInfoDict["collectionContentInfo"] = self.collectionInfoDict
        ncl(self.collectionInfoDict)
        s = json.dumps(self.additionalInfoDict, sort_keys=True, indent=4)
        infoFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.workingDir, "."+gInfoFileExt, gInfoFilePrefix))
        logFile = open(infoFilePath, 'w')
        logFile.write(s)
        logFile.kill_console_process_tree()
        self.getZipFile().addfile(unicode(infoFilePath), unicode(infoFilePath))
        self.package_file.kill_console_process_tree()
        #Set attribute so new zip will be created if this object is still in use
        self.package_file = None
        self.additionalInfoDict = {}
        return self.package_file_full_path
    
    def enumItems(self, archiveFullPath):
        zipFile = zipClass.ZFile(archiveFullPath, 'r')
        for i in zipFile.list():
            print 'enumItems------------------------------', "^"+gInfoFilePrefix + ".*" + "\."+gInfoFileExt + "$", i
            print i
            #i would be like: "tmp/working/zippedCollFile1330392748.82.log"
            if not (re.search("^(.+\/)*"+gInfoFilePrefix + ".*" + "\."+gInfoFileExt + "$", i) is None):
                print 'enumItems------------------------------'
                print i
                infoFilePath = zipFile.extract(i, self.workingDir)
                print 'returning ----------'
                yield infoFilePath
            
    def enumZippedFiles(self, archiveFullPath):
        zipFile = zipClass.ZFile(archiveFullPath, 'r')
        for i in zipFile.list():
            if (re.search("^"+gInfoFilePrefix + ".*" + "\."+gInfoFileExt + "$", i) is None):
                yield zipFile.extract(i, self.workingDir)
    ################################################
    # The following functions are not recommended to be called from outside of this class
    def getZipFile(self):
        if self.package_file is None:
            self.package_file_full_path = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.workingDir, '.zip'))
            self.package_file = zipClass.ZFile(self.package_file_full_path, 'w')
        return self.package_file
    
    
