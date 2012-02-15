import libSys
import libs.utils.webUtils as webUtils
#import libs.collection.collectionManager as collectionManager
#import apps.fileSystem.collectionListItemsV3 as collectionListItems
import libs.html.response
#import libs.ufsDb.ufsDbSys as dbSys
import libs.utils.objTools as objTools
import libs.utils.stringTools as stringTools
import libs.tree.jsTreeItemWithCollectionBackend as jsTreeItemWithCollectionBackend
gDebugFlag = True#False
import libs.ufs.ufs as ufs
import libs.tree.jsTreeNamedItemFuncV3 as jsTreeNamedItemFunc
import libs.ufs.ufsTreeItem as ufsTreeItem
import libs.collection.collectionManager as collectionManager
import libs.services.servicesV2 as service


def jqueryListOnCollection(req):
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"collectionId":u"-1"}, req.getQueryInfo())
    #Get collection from system, collection system contains cached collections and filesystem collections.
    if not objTools.isUuid(param["collectionId"]):
        #It is not uuid://xxxx-xxx-xxx-xxx-xxxx-xxxx
        param["collectionId"] = stringTools.jsIdDecoding(param["collectionId"])
    #Output
    req.resp.genJsonHead()
    if param["collectionId"] == "-1":
        p = ufs.ufsTreeUuidItem()
    #res = path
    else:
        #p = desktopApp.lib.localTreeItem.localTreeItem(path.decode('utf8'))
        if objTools.isUfsUrl(param["collectionId"]):#try:
            p = ufsTreeItem.getUfsTreeItem(param["collectionId"], req)
            #print "after getufstreeitem"
            #res += str(p.listNamedChildren())
        else:#except ValueError:
            #No schema/protocol string. Normal dir
            p = jsTreeItemWithCollectionBackend.jsTreeItemWithCollectionBackend(param["collectionId"], None, req.getDbSys())
    #Get the checked elements in the tree
    try:
        co = collectionManager.getCollection(u"uuid://3b84d155-cc5c-428e-8009-12d5fdc68b2a", req.getDbSys()).getRange(0, None)
    except KeyError:
        co = []
    #print "before containerListJson"
    data = jsTreeNamedItemFunc.containerListJson(p, checkedItems=co)

    #print data
    if data == u"":
        raise "no item, raise exception to prevent loop query"
    req.resp.write(data)
    req.resp.end()
    
    
class prosedoParam:
    def getAllFieldStorageUnicode(self):
        return {u"collectionId": u"winUfs_0_1_1290b5fcc-be54-4ae4-9613-20a24de723cf"}
    
    
class prosedoReq:
    def getQueryInfo(self):
        return prosedoParam()
    
    
if __name__=='__main__':
    jqueryListOnCollection(service.req())
    #jqueryListOnCollection(prosedoReq())