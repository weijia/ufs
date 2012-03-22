import libSys
import libs.utils.webUtils as webUtils
import libs.utils.objTools as objTools
import libs.utils.stringTools as stringTools

import libs.ufs.ufsV2 as ufs
import libs.collection.collection2Json as collection2Json
import libs.ufs.ufsCollection as ufsCollection
import libs.collection.collectionManager as collectionManager
import libs.services.servicesV2 as service


gDebugFlag = True#False
gCheckedCollectionId = u"uuid://3b84d155-cc5c-428e-8009-12d5fdc68b2a"

def jqueryListOnCollection(req):
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"collectionId":u"-1", u"tree":u"n", u"start":0, u"cnt":40}, req.getQueryInfo())
    #print param

    if param["collectionId"] == "-1":
        ####################################
        # It is the root element of the tree
        ####################################
        collectionItemList = ufs.ufsRootItem()
    elif not objTools.isUuid(param["collectionId"]):
        #############################################
        #It is not uuid://xxxx-xxx-xxx-xxx-xxxx-xxxx
        #############################################
        param["collectionId"] = stringTools.jsIdDecoding(param["collectionId"])
        if not objTools.isUfsUrl(param["collectionId"]):
            param["collectionId"] = u"file:///"+param["collectionId"]
        #Change URL to file:///D:/tmp etc.
        collectionItemList = ufsCollection.getUfsCollection(param["collectionId"], req)
    req.resp.genJsonHead()
    #print collectionItemList.listNamedChildren(0, 40, False)
    ##############################################
    # Get checked item for tree
    ##############################################
    try:
        checkedItemList = collectionManager.getCollection(gCheckedCollectionId, req.getDbSys()).getRange(0, None)
    except KeyError:
        checkedItemList = []
    #print "before containerListJson"
    # Check if we are generating the tree.
    if param["tree"] == u"n":
        #print "false"
        isTree = False
        start = int(param["start"])
        cnt = int(param["cnt"])
    else:
        isTree = True
        start = 0
        cnt = None
    #print start, cnt
    #print >>sys.stderr, "-------------", start, cnt
    #data = "1"
    ####################################################
    # Generate JSON string for collection
    ####################################################
    data = collection2Json.containerListJson(collectionItemList, start, cnt, isTree, req, checkedItemList)
    
    #print data
    if data == u"":
        raise "no item, raise exception to prevent loop query"
    req.resp.write(data)
    req.resp.end()
    
    
    
if __name__=='__main__':
    param = {u"collectionId": u"D_0_1oldmachine_1TDDOWNLOAD", "start":"40", "cnt": "40"}
    param = None
    jqueryListOnCollection(service.req(param))