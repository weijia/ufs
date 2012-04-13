import localLibSys
from zippedInfo import zippedInfo

gWorkingDir = "d:/tmp/working"

class zippedInfoWithContent(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(zippedInfoWithContent, self).__init__(workingDir)
    def addItem(self, itemObj):
        super(zippedInfoWithContent, self).addItem(itemObj)
        fullPath = itemObj["fullPath"]
        #Add file to zip
        return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
