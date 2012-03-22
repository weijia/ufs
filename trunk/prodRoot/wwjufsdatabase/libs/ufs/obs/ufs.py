#import libSys
import ufsTreeItem
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
import libs.utils.odict as odict

ufsRootItemUuid = u'3fe6382b-0219-40c7-add3-2f3b60aeb368'


def localDriverExist():
    if True:#try:
        import localLibSys
        import localLibs.windows.winUfs as winUfs
        return True
    else:#except ImportError:
        return False


def getUfsUuidItemUrl(itemId = ufsRootItemUuid):
    return u"uuid"+configurationTools.getFsProtocolSeparator()+itemId
    
class ufsTreeUuidItem(ufsTreeItem.ufsTreeItemBase):
    def __init__(self, id = ufsRootItemUuid):
        self.id = id
    def isContainer(self, fullPath):
        '''
        return os.path.isdir(p)
        '''
        return True

    def child(self, childId):
        if winUfsRootItemUuid == childId:
            return winUfs.winUfsTreeItem()
        return ufsTreeUuidItem(childId)
        
    def listNamedChildren(self, start = 0, cnt = None, getParent = True):
        #Return {fullPath:name}
        db = dbSys.dbSysSmart()
        #print "retriving co:", getUfsUuidItemUrl(self.id)
        co = collectionManager.getCollection(getUfsUuidItemUrl(self.id), db).getRange(0, None)
        #res = {getUfsUuidItemUrl(self.id):getUfsUuidItemUrl(self.id)}
        #res = {}
        #print "got co:", co
        res = odict.OrderedDict()
        #res["test"] = co
        #Hard code the freq items
        res[u"freq://root"] = u"Freqently Used"
        #Hard code the tag system
        res[u"tag://,"] = u"Tag System"
        #Hard code the task system
        res[u"tasklist://,"] = u"Task List"
        #Add other item in root item
        ns = nameService.nameService(db.getNameServiceDb())
        for i in co:
            n = ns.getName(i)
            if n is None:
                try:
                    #Get url
                    n = objTools.getUrlContent(i)
                except ValueError:
                    n = None
            if n is None:
                #Seems to be a directory path
                try:
                    n = objTools.getUfsBasename(i)
                except:
                    n = None
            if n is None:
                n = i
            res[i] = n
        if localDriverExist():
            res[u"winUfs"+configurationTools.getFsProtocolSeparator()+winUfs.winUfsRootItemUuid] = u"Filesystem"
        return res


def getUfsTreeItem(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return ufsTreeUuidItem(itemUrl, req)
