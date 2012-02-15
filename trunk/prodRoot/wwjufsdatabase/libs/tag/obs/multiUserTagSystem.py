import inheritableExclusableTagSystem
import libSys
import libs.collection.cachedCollection as cachedCollection
import libs.ufsDb.dbSys as dbSys
import tagSystemV2
import sessionBase as sessionBase

'''
class tagSystemShoveDb(inheritableExclusableTagSystem.tagSystemShoveDb):
    #def __init__(self, dbSysInst = dbSys.dbSysSmart(sessionBase.sessionInstanceBase('weijia')), otherDbSysInstList = [dbSys.dbSysSmart()]):
    def __init__(self, dbSysInst = dbSys.dbSysSmart(), 
        otherDbSysInstList = [dbSys.dbSysSmart(sessionBase.sessionInstanceBase('weijia'))], dbSupportsCnt = False):
        self.otherTagSys = []
        for i in otherDbSysInstList:
            self.otherTagSys.append(inheritableExclusableTagSystem.tagSystemShoveDb(i))
        inheritableExclusableTagSystem.tagSystemShoveDb.__init__(self, dbSysInst, dbSupportsCnt)

    def getTags(self, url):
        res = list(inheritableExclusableTagSystem.tagSystemShoveDb.getTags(self, url))
        for i in self.otherTagSys:
            res.extend(list(i.getTags(url)))
        return list(set(res))
'''


if __name__ == '__main__':
    #dbSysInst = dbSys.dbSysSmart(sessionBase.sessionInstanceBase('weijia'))
    #dbNew = tagSys.tagSystemShoveDb(dbSysInst)
    dbOld = tagSystemShoveDb()
    res = {}
    
    for i,j in dbOld.getAllTags():
        print 'find tag:',i,j
        for url in dbOld.enumObjsWithTag(i):
            print url.encode('gbk','replace'),i.encode('gbk','replace'),j
            if res.has_key(url):
                res[url].append(i)
            else:
                res[url] = [i]
    '''
    for i in res:
        if os.path.exists(i):
            dbNew.tag(i, list(set(res[i])))
        else:
            print i.encode('gbk','replace'), str(list(set(res[i]))).encode('gbk','replace')
    '''
