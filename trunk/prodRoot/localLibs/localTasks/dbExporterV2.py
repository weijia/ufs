import localLibSys

import wwjufsdatabase.libs.ufsDb.ufsDbSys as dbSys
import wwjufsdatabase.libs.utils.simplejson as json
from optparse import OptionParser
import wwjufsdatabase.libs.tag.sessionBase as sessionBase
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.configurationTools as cfg
import os
import wwjufsdatabase.libs.encryption.arc4Encryptor as enc
import md5


def dictListEncryptor(dictList, password):
    e = enc.encryptor()
    res = []
    for i in dictList:
        values = i["value"]
        encryptedValues = []
        for j in values:
            print j.encode('gbk', 'replace')
            encryptedValues.append(e.en(j, password))
        j = {"db": i["db"], "user": i["user"], "key":e.en(i["key"], password), "value":encryptedValues,
            "encHash":unicode(md5.new(password).hexdigest())}
        res.append(j)
    return res

    
def dictListDecryptor(dictList, password):
    e = enc.encryptor()
    res = []
    for i in dictList:
        values = i["value"]
        decryptedValues = []
        for j in values:
            v = e.de(j, password)
            d = decryptedValues.append(v)
            #print v.encode('gbk', 'replace')
        j = {"db": i["db"], "user": i["user"], "key":e.de(i["key"], password), "value":decryptedValues}
        res.append(j)
    return res

    
def backupDbSingle(dbName, targetDir, password, user, afterTimeStamp, beforeTimeStamp):
    if user is None:
        dbSysInst = dbSys.dbSysSmart()
    else:
        dbSysInst = dbSys.dbSysSmart(sessionBase.sessionInstanceBase(user))
        

    db = dbSysInst.getDb(dbName)
    res = []

    if not os.path.exists(targetDir):
        misc.ensureDir(targetDir)
    for i in db.keysDuring(afterTimeStamp, beforeTimeStamp):
        #print i
        #values = db.testFunc(i)
        values = db[i]
        j = {"db": dbName, "user": user, "key":i, "value":values, "t": beforeTimeStamp}
        res.append(j)
        
    return res
    
def backupDbAuto(dbName, targetDir, password, user, timeStamp):
    finalRes = []
    if user is None:
        dbSysInst = dbSys.dbSysSmart()
    else:
        dbSysInst = dbSys.dbSysSmart(sessionBase.sessionInstanceBase(user))
    beforeTimeStamp = dbSysInst.getTimeStamp()
        
    if dbName is None:
        dbList = dbSysInst.getDbNameList()
    else:
        dbList = [dbName]
    for i in dbList:
        print i
        
        res = backupDbSingle(i, targetDir, password, user, timeStamp, beforeTimeStamp)
        finalRes.extend(res)
    #res = dictListEncryptor(res, password)
    #res = dictListDecryptor(res)
    s = json.dumps(finalRes, sort_keys=True, indent=4)
    #s = json.dumps(finalRes)
    f = open(os.path.join(targetDir, str(dbName)+'_for_user_'+str(user)+'.json'),'w')
    f.write(s)
    f.close()
    dbSysInst = dbSys.dbSysSmart()
    c = cfg.configuration(dbSysInst)
    c[u"mongoBackupTimeStamp"] = beforeTimeStamp

            

def main():
    parser = OptionParser()
    parser.add_option("-u", "--user", action="store",help="username for the database system",default = None)
    parser.add_option("-p", "--password", action="store",help="password for target output",default = u'defaultPASS123')
    parser.add_option("-t", "--targetDir", action="store", help="database backup target directory",default = 'd:/tmp/backup')
    parser.add_option("-n", "--name", action="store", help="database name for backup",default = None)
    parser.add_option("-s", "--show", action="store", help="print time stamp of last backup",default = None)
    parser.add_option("-r", "--reset", action="store", help="reset backup timestamp",default = None)
    
    
    
    (options, args) = parser.parse_args()
    dbSysInst = dbSys.dbSysSmart()
    c = cfg.configuration(dbSysInst)
    
    if not (options.reset is None):
        del c[u"mongoBackupTimeStamp"]
        return
    
    if not c.has_key(u"mongoBackupTimeStamp"):
        t = None
    else:
        t = c[u"mongoBackupTimeStamp"]
    
    
    if not (options.show is None):
        print c[u"mongoBackupTimeStamp"]
        return
    #print options,args
    #tv = comparer.getMecacoreVector(options.case,options.tf,options.blk,options.point,options.ant)
    backupDbAuto(options.name, options.targetDir, options.password, options.user, t)

        
        
    
if __name__ == '__main__':
    main()
