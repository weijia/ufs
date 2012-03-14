import localLibSys
from zippedInfo import zippedInfo

gWorkingDir = "d:/tmp/working"

class zippedCollectionWithInfo(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(zippedCollectionWithInfo, self).__init__(workingDir)
    def addItem(self, fullPath):
        super(zippedCollectionWithInfo, self).addItem(fullPath)
        #Add file to zip
        return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
