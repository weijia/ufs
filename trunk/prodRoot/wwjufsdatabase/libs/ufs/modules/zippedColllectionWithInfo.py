#import libSys
import libs.collection.collectionManager as collectionManager
import libs.ufsDb.dbSys as dbSys
import libs.services.nameServiceV2 as nameService
import libs.utils.configurationTools as configurationTools
import libs.utils.objTools as objTools

import libs.utils.odict as odict



def getUfsUuidItemUrl(itemId = ufsRootItemUuid):
    return u"uuid"+configurationTools.getFsProtocolSeparator()+itemId
    
class fileCollection:
    def __init__(self, fullPath, objDb):
        self.fullPath = fullPath
        self.objDb = objDb
    def listNamedChildren(self, start, cnt, isTree):
        pass
    def isChildContainer(self, child):
        pass



def getUfsTreeItem(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return fileCollection(itemUrl, req)
