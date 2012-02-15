import libSys
import libs.ufsDb.dbSys as dbSys
import libs.utils.webUtils as webUtils
import libs.collection.collectionBase as collectionBase
import libs.utils.simplejson as json
import libs.html.response

def importCollectionFromJson(jsonCollectionStr, htmlGen):
    r = json.loads(jsonCollectionStr)
    dbInst = dbSys.dbSysSmart()
    for i in r:
        c = collectionBase.collectionBase(i, dbInst.getCollectionDb())
        try:
            htmlGen.write(r[i]+u"<br>")
        except:
            pass
        if type(r[i]) == list:
            for j in r[i]:
                c.append(j)
        else:
            c.append(r[i])
            
    
def handleImportCollectionFromJsonRequest():
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"jsonCollection":-1})
    h = libs.html.response.html()
    h.genHead('Upload Collections')
    if param[u"jsonCollection"] == -1:
        h.genForm('/apps/collection/collectionImporter.py',[['f','jsonCollection']])
    else:
        importCollectionFromJson(param[u"jsonCollection"], h)
        h.write('-------------------------------------------')
        h.write(param[u"jsonCollection"])
    h.genEnd()

    
if __name__=='__main__':
    handleImportCollectionFromJsonRequest()