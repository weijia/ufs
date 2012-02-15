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

def collectionListItem(iter, req, divClassName = u"thumbDiv", imgClass=u"thumbImage", tagName=u"li"):
    thumbViewScript = u"http://localhost:8805/thumb?path="
    res = ""
    for i in iter:
        res +=u'<%s class="%s">'%(tagName, divClassName+ " ui-widget-content")
        t = tagSys.getTagSysObj(req.getDbSys())
        #print '----------------------------------------------------'
        #print i
        tList = t.getTags(i)
        tagStr = u""
        '''
        for k in tList:
            tagStr += k.decode('utf8')
        '''
        tagStr = u','.join(tList)
        '''
        res += '<div class="elementTag" path=%s>'%urllib.quote(i)
        res += ','.join(tList)
        res += 'default'
        res += '</div>'
        '''
        if tagStr == u"":
            tagStr = u"input tag"
        #quote can not support unicode, see http://bugs.python.org/issue1712522
        encoded = urllib.quote(encodingTools.translateToPageEncoding(i))
        res += u'<img class="%s" src="%s%s" path="%s"/><p class="tagEditor">%s</p>'%(imgClass, 
            thumbViewScript, encoded, i, tagStr)#first encode the str, so the browser can decode the string to local encoding
        res +=u'<div class="placeholder"></div>'
        res += u'</%s>\n'%tagName
    return res



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
        res = collectionListItem(co, req)
    else:#except:
        pass
    #h = libs.html.response.html()
    #print "hello"
    #h.write("good")
    req.resp.genPartialHtmlHead()
    req.resp.write(res)
    #h.write(l.s)
    #print res
    req.resp.end()
    
    
    
    
if __name__=='__main__':
    jqueryListOnCollection(service.req())