import libSys
import libs.utils.webUtils as webUtils
import libs.collection.collectionManager as collectionManager
#import webapproot.apps.fileSystem.collectionListItemsV3 as collectionListItems
import libs.html.response
#import libs.ufsDb.ufsDbSys as dbSys
import libs.utils.objTools as objTools
#import libs.tag.multiUserTagSystem as tagSystem
import libs.tag.tagSystemInterface as tagSys
import urllib
import libs.utils.stringTools as stringTools
import libs.utils.encodingTools as encodingTools
import libs.services.servicesV2 as service
import libs.utils.simplejson as json

def collectionListItem(iter, req):
    resList = []
    for i in iter:
        t = tagSys.getTagSysObj(req.getDbSys())
        tList = t.getTags(i)
        #encoded = urllib.quote(encodingTools.translateToPageEncoding(i))
        resList.append({"path":i, "tags":tList})
    return resList



def jqueryListOnCollection(req):
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"collectionId":u"C:/",u"start":0,u"cnt":40}, req.getQueryInfo())
    #Get collection from system, collection system contains cached collections and filesystem collections.
    #h.write("<!--")
    #print "hello"
    print param
    if not objTools.isUuid(param["collectionId"]):
        #param["collectionId"] = collectionListItems.jsIdEncoding(param["collectionId"])
        param["collectionId"] = stringTools.jsIdDecoding(param["collectionId"])
    #h.write(unicode(str(int(param["start"])))+unicode(str(int(param["cnt"]))))
    co = collectionManager.getCollection(param["collectionId"], req.getDbSys()).getRange(int(param["start"]), int(param["cnt"]))

    #Output
    #h.write(str(co))
    #res = ""
    #h.write("-->")
    if True:#try:
        resList = collectionListItem(co, req)
    else:#except:
        pass
    #h = libs.html.response.html()
    #print "hello"
    #h.write("good")
    req.resp.genJsonHead()
    req.resp.write(json.dumps(resList, indent = 4))
    #h.write(l.s)
    #print res
    req.resp.end()
    
    
    
    
if __name__=='__main__':
    jqueryListOnCollection(service.req())