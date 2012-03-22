import ufsTreeItem
'''
import libs.collection.collectionManager as collectionManager
import libs.ufsDb.dbSys as dbSys
import libs.services.nameServiceV2 as nameService
import libs.utils.configurationTools as configurationTools
import libs.utils.objTools as objTools

try:
    import localLibSys
    import localLibs.windows.winUfs as winUfs
except ImportError:
    pass
'''
class tasklistTreeItem(ufsTreeItem.ufsTreeItemBase):
    def __init__(self, itemId, req):
        self.id = itemId
        self.req = req
    def isContainer(self, fullPath):
        '''
        return os.path.isdir(p)
        '''
        return True
        pass

    def child(self, childId):
        '''
        return abspath
        '''
        return "tasklist://"
        pass
        
    def listNamedChildren(self):
        #Return {fullPath:name}
        return {u"tasklist://running":u"running",u"tasklist://all":u"all",}

def getUfsTreeItem(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return tasklistTreeItem(itemUrl, req)
