import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
import localLibs.objSys.ufsObj as ufsObj
import localLibs.compress.zipClass as zipClass
from zippedInfo import zippedInfo
from localLibs.thumb.thumbInterface import getThumb
import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.storage.infoCollectors.ThumbCollector import ThumbCollector
from localLibs.logSys.logSys import *

gWorkingDir = "d:/tmp/working"
gDefaultInfoSize = 100

class zippedInfoWithThumb(zippedInfo):
    def __init__(self, workingDir = gWorkingDir, thumbDir = gWorkingDir):
        super(zippedInfoWithThumb, self).__init__(workingDir)
        self.dbInst = objectDatabase.objectDatabase()
        self.thumb_collector = ThumbCollector(thumbDir)
        
    def addItem(self, itemObj):
        return self.addThumb(itemObj)
    
    def addThumb(self, itemObj):
        self.thumb_collector.collect_thumb(itemObj, )