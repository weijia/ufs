import localLibSys
from zippedInfo import zippedInfo

gWorkingDir = "d:/tmp/working"

class zippedCollectionWithInfo(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(zippedCollectionWithInfo, self).__init__(workingDir)
    def addItem(self, itemObj):
        super(zippedCollectionWithInfo, self).addItem(itemObj)
        fullPath = itemObj["fullPath"]
        #Add file to zip
        return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
