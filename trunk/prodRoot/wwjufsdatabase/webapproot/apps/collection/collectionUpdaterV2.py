import libSys
import libs.ufsDb.dbSys as dbSys
import libs.utils.webUtils as webUtils
import libs.collection.collectionBase as collectionBase
import libs.utils.simplejson as json
import libs.services.servicesV2 as service
import libs.collection.collectionManagerV2 as collectionManager
import libs.utils.stringTools as stringTools
import libs.utils.objTools as objTools

def updateCollectionFromJson(jsonCollectionStr, htmlGen, dbInst):
    r = json.loads(jsonCollectionStr)
    for k in r:
        data = r[k]
        for i in data:        
            c = collectionManager.getCollection(i, dbInst)
            if k == "add":
                op = c.append
            if k == "del":
                op = c.remove
            if k == "update":
                c.removeAll()
                op = c.append
            
            if type(data[i]) == list:
                for idInCol in data[i]:
                    objFullPath = stringTools.jsIdDecoding(idInCol)
                    objUfsUrl = objTools.getUfsUrl(objFullPath)
                    htmlGen.write(u"%s:"%k+objUfsUrl+u"<br>")
                    #continue
                    op(objUfsUrl)
            else:
                idInCol = data[i]
                objFullPath = stringTools.jsIdDecoding(idInCol)
                objUfsUrl = objTools.getUfsUrl(objFullPath)
                htmlGen.write(u"%s:"%k+objUfsUrl+u"<br>")
                #continue
                op(objUfsUrl)


        
        
        
def handleImportCollectionFromJsonRequest(req):
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"jsonCollection":-1}, req.getQueryInfo())
    h = req.resp
    h.genHead('Upload Collections')
    if param[u"jsonCollection"] == -1:
        h.genForm('/apps/collection/collectionImporter.py',[['f','jsonCollection']])
    else:
        dbInst = req.getObjDbSys()
        updateCollectionFromJson(param[u"jsonCollection"], h, dbInst)
        h.write('-------------------------------------------')
        h.write(param[u"jsonCollection"])
    h.genEnd()

    
if __name__=='__main__':
    handleImportCollectionFromJsonRequest(service.req())
