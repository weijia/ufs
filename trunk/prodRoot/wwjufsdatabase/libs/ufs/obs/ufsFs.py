import libs.ufsDb.dbSys as dbSys
import ufs
import libs.collection.collectionManager as collectionManager
import libs.services.nameServiceV2 as nameService
import libs.utils.objTools as objTools

class ufsUploadedTreeItem(ufs.ufsTreeUuidItem):
    def listNamedChildren(self, start = 0, cnt = None, getParent = True):
        #Return {fullPath:name}
        db = dbSys.dbSysSmart()
        co = collectionManager.getCollection(u"ufsFs://"+self.id, db).getRange(0, None)
        #res = {getUfsUuidItemUrl(self.id):getUfsUuidItemUrl(self.id)}
        res = {}
        #res["test"] = co
        ns = nameService.nameService(db.getNameServiceDb())
        for i in co:
            n = ns.getName(i)
            if n is None:
                n = i
            res[i] = objTools.getUfsBasename(n)
        return res




def getUfsTreeItem(itemUrl, req):
    #The itemUrl does not include the protocol part
    #For example: for uuid://xxxxx-xxxxx itemUrl will be xxxxx-xxxxx
    return ufsUploadedTreeItem(itemUrl)
