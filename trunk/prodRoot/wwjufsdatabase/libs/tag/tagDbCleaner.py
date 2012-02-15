import libSys
#import libs.tag.inheritableExclusableTagSystem as tagSys
import libs.tag.tagSystemV2 as tagSys

import libs.ufsDb.dbSys as dbSys
import os
import libs.utils.misc as misc
import libs.ufsDb.ufsDbSys as newDbSys

import sessionBase as sessionBase


def main():
    dbSysInst = dbSys.dbSysSmart()
    newDbSysInst = newDbSys.dbSysSmart()
    dbNew = tagSys.tagSystemShoveDb(newDbSysInst)
    dbOld = tagSys.tagSystemShoveDb(dbSysInst, dbSupportsCnt=True)
    res = {}
    
    for i,j in dbOld.getAllTags():
        print 'find tag:',i,j
        for url in dbOld.enumObjsWithTag(i):
            print url.encode('gbk','replace'),i.encode('gbk','replace'),j
            if res.has_key(url):
                res[url].append(i)
            else:
                res[url] = [i]
            
    for i in res:
        if os.path.exists(i):
            dbNew.tag(i, list(set(res[i])))
            pass
        else:
            print i.encode('gbk','replace'), str(list(set(res[i]))).encode('gbk','replace')

    
if __name__=='__main__':
    main()