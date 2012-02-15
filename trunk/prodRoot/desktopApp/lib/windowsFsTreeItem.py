from localTreeItemBase import localTreeItemBase as localTreeItemBase
from localTreeItemBase import localFilesystemDecode as localFilesystemDecode
from libs.localDb.dictShoveDb import getDb



        
class windowsFsTreeItem(localTreeItemBase):
    def __init__(self, fullUrl):
        self.fullUrl = fullUrl

    def getName(self, p):
        return os.path.basename(p)
        
    def isContainer(self, p):
        '''
        return os.path.isdir(p)
        '''
        try:
            l = os.listdir(p)
            if len(l) > 0:
                return True
            return False
        except WindowsError:
            return False

    def child(self, fullPath):
        return vfsLocalTreeItemBase(fullPath)