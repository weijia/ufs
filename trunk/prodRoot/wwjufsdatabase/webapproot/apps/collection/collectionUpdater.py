import libSys
import libs.ufsDb.dbSys as dbSys
import libs.utils.webUtils as webUtils
import libs.collection.collectionBase as collectionBase
import libs.utils.simplejson as json
import libs.services.servicesV2 as service


def updateCollectionFromJson(jsonCollectionStr, htmlGen, dbInst):
    r = json.loads(jsonCollectionStr)
    for k in r:
        if k == "add":
            data = r[k]
            for i in data:
                c = collectionBase.collectionBase(i, dbInst.getCollectionDb())
                try:
                    htmlGen.write(u"adding:"+r[i]+u"<br>")
                except:
                    pass
                if type(data[i]) == list:
                    for j in data[i]:
                        c.append(j)
                else:
                    c.append(data[i])
        elif k == "del":
            data = r[k]
            for i in data:
                c = collectionBase.collectionBase(i, dbInst.getCollectionDb())
                try:
                    htmlGen.write(u"removing:"+r[i]+u"<br>")
                except:
                    pass
                if type(data[i]) == list:
                    for j in data[i]:
                        c.remove(j)
                else:
                    c.remove(data[i])
                    
        
        elif k == "update":
            data = r[k]
            for i in data:
                c = collectionBase.collectionBase(i, dbInst.getCollectionDb())
                try:
                    htmlGen.write(u"removing:"+r[i]+u"<br>")
                except:
                    pass
                l = data[i]
                if type(l) == unicode:
                    l = [l]
                c.update(l)

        
        
        
def handleImportCollectionFromJsonRequest(req):
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"jsonCollection":-1}, req.getQueryInfo())
    h = req.resp
    h.genHead('Upload Collections')
    if param[u"jsonCollection"] == -1:
        h.genForm('/apps/collection/collectionImporter.py',[['f','jsonCollection']])
    else:
        dbInst = dbSys.dbSysSmart()
        updateCollectionFromJson(param[u"jsonCollection"], h, dbInst)
        h.write('-------------------------------------------')
        h.write(param[u"jsonCollection"])
    h.genEnd()

    
if __name__=='__main__':
    handleImportCollectionFromJsonRequest(service.req())
