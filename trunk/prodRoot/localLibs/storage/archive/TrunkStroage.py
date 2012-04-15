#import re
import localLibSys
#import wwjufsdatabase.libs.utils.simplejson as json
#import wwjufsdatabase.libs.utils.transform as transform
#import localLibs.objSys.ufsObj as ufsObj
#import wwjufsdatabase.libs.utils.fileTools as fileTools
from localLibs.logSys.logSys import *
from localLibs.storage.infoStorage.zippedInfo import zippedInfo

gWorkingDir = "d:/tmp"

class TrunkStorageInterface(object):
    def __init__(self):
        pass
    
    def add_file(self, itemObj):
        pass
    
    def finalize_one_trunk(self):
        pass
    
    def add_info(self, infoDict):
        pass
    

    
class TrunkStorage(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(TrunkStorage, self).__init__(workingDir)
        
    def add_info(self, infoDict):
        self.addAdditionalInfo(infoDict)
            
    def add_file(self, itemObj):
        fullPath = itemObj["fullPath"]
        self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))


    def finalize_one_trunk(self):
        #Add info to zip file
        return self.finalizeOneTrunk()