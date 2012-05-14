#import ufsTreeItem
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
import libs.tag.tagSystemInterface as tagSys
import libs.utils.odict as odict
from UfsModuleBase import UfsModuleBase

class tagCollectionItem(UfsModuleBase):
    def __init__(self, itemId, req):
        super(tagCollectionItem, self).__init__()
        self.tagS = tagSys.getTagSysObj(req.getDbSys())
        print '--------------------------------tagCollectionItem'
        self.itemId = itemId
        
    
    def isChildContainer(self, child):
        return False

        
    def listNamedChildren(self, start, cnt, isTree):
        '''
        Shall return res = {"D:/file/full/path/filename": "filename",... }
        '''
        #Return {fullPath:name}
        res = odict.OrderedDict()
        cnt = 0
        #import sys
        #print >>sys.stderr, "listing children"
        for i, j in self.tagS.getAllTags():
            res[u"tag://,"+i] = i + u"("+unicode(str(j))+u")"
            cnt += 1
            if cnt > 10:
                break
        return res


def getUfsCollection(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return tagCollectionItem(itemUrl, req)
