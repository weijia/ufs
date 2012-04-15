import localLibSys
from zippedInfo import zippedInfo

gWorkingDir = "d:/tmp/working"

class zippedInfoWithContent(zippedInfo):
    def __init__(self, workingDir = gWorkingDir):
        super(zippedInfoWithContent, self).__init__(workingDir)
        
    def addItem(self, itemObj):
        #Call super class to store item info, this info will
        #be saved when a trunk is finalized.
        super(zippedInfoWithContent, self).addItem(itemObj)
        self.addFileContent(itemObj)
        
    def addFileContent(self, itemObj):
        fullPath = itemObj["fullPath"]
        #Add file to zip
        return self.getZipFile().addfile(unicode(fullPath), unicode(fullPath))
