import ufsTreeItem
import ufsV2
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
class exampleTreeItem(ufsTreeItem.ufsTreeItemBase):
    def __init__(self, itemId = ufsV2.ufsRootItemUuid):
        pass
    def isContainer(self, fullPath):
        '''
        return os.path.isdir(p)
        '''
        pass

    def child(self, childId):
        '''
        return abspath
        '''
        pass
        
    def listNamedChildren(self):
        #Return {fullPath:name}
        pass


def getUfsTreeItem(itemUrl):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return exampleTreeItem(itemUrl)
