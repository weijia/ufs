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
#import wwjufsdatabase.libs.tag.tagSystemInterface as tagSys
import wwjufsdatabase.libs.utils.odict as odict
from wwjufsdatabase.libs.ufs.modules.UfsModuleBase import UfsModuleBase
import localLibSys
from localLibs.logSys.logSys import *
#from localLibs.services.beanstalkdServices.FileArchiveServiceV2 import g_file_archive_storage_collection_id

class StorageCollectionItem(UfsModuleBase):
    def __init__(self, item_id, req):
        #The itemUrl does not include the protocol part
        #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
        super(StorageCollectionItem, self).__init__()
        self.obj_db = req.getObjDbSys()
        self.item_id = item_id
        
    
    def isChildContainer(self, child):
        return False

        
    def listNamedChildren(self, start, cnt, isTree):
        '''
        Shall return res = {"D:/file/full/path/filename": "filename",... }
        '''
        #Return {fullPath:name}
        res = odict.OrderedDict()
        cnt = 0
        col = self.obj_db.getCollection(u"zip_file_storage://"+self.item_id)
        #print "start enum"
        for i in col.enumObjsInRange(start, cnt):
            res[unicode(i.getIdInCol())] = unicode(i.getIdInCol())
        #print "returning items"
        return res
            


def getUfsCollection(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return StorageCollectionItem(itemUrl, req)
