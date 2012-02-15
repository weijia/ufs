import localLibSys

import wwjufsdatabase.libs.ufsDb.ufsDbSys as dbSys
import wwjufsdatabase.libs.utils.simplejson as json
from optparse import OptionParser
import wwjufsdatabase.libs.tag.sessionBase as sessionBase
import wwjufsdatabase.libs.utils.misc as misc
import os
import wwjufsdatabase.libs.encryption.arc4Encryptor as enc

import md5

def backupDbSingle(dbName, targetDir, password, user):
    if user is None:
        dbSysInst = dbSys.dbSysSmart()
    else:
        dbSysInst = dbSys.dbSysSmart(sessionBase.sessionInstanceBase(user))
        

    db = dbSysInst.getDb(dbName)
    res = []
    e = enc.encryptor()
    if not os.path.exists(targetDir):
        misc.ensureDir(targetDir)
    for i in db.keys():
        #print i
        #values = db.testFunc(i)
        values = db[i]
        encryptedValues = []
        for i in values:
            print i.encode('gbk', 'replace')
            encryptedValues.append(e.en(i, password))
        j = {"key":e.en(i, password), "value":encryptedValues,
            "encHash":unicode(md5.new(password).hexdigest())}

        res.append(j)
        
    #print res
    s = json.dumps(res, sort_keys=True, indent=4)
    f = open(os.path.join(targetDir, dbName+'_for_user_'+str(user)+'.json'),'w')
    f.write(s)
    f.close()

def backupDbAuto(dbName, targetDir, password, user):
    if user is None:
        dbSysInst = dbSys.dbSysSmart()
    else:
        dbSysInst = dbSys.dbSysSmart(sessionBase.sessionInstanceBase(user))
        
    if dbName is None:
        for i in dbSysInst.getDbNameList():
            print i
            backupDbSingle(i, targetDir, password, user)
    else:
        backupDbSingle(dbName, targetDir, password, user)

def main():
    parser = OptionParser()
    parser.add_option("-u", "--user", action="store",help="username for the database system",default = None)
    parser.add_option("-p", "--password", action="store",help="password for target output",default = u'defaultPASS123')
    parser.add_option("-t", "--targetDir", action="store", help="database backup target directory",default = 'd:/tmp/backup')
    parser.add_option("-n", "--name", action="store", help="database name for backup",default = None)
    '''
    parser.add_option("-b", "--blk", action="store", help="block number",default = None, type="int")
    parser.add_option("-a", "--ant", action="store", help="antenna number, 0: 1 ant, 1:2 ant",default = 0, type="int")
    parser.add_option("-f", "--file", action="store", help="captured data file path")
    parser.add_option("-s", "--symbolIndexStart", action="store", help="the start of symbol index for the data",default = 0, type="int")
    parser.add_option("-e", "--symbolIndexEnd", action="store", help="the end of symbol index for the data",default = 0, type="int")
    parser.add_option("-i", "--cellId", action="store", help="the cell id of the config",default = 0, type="int")
    parser.add_option("-w", "--bandwidthIndex", action="store", help="current bandwidth index, 2 for 5MHz, 3 for 10Mhz, 5 for 20Mhz",default = -1, type="int")
    parser.add_option("-y", "--curSym", action="store", help="current comparing symbol",default = 0, type="int")
    parser.add_option("-j", "--justPass", action="store", help="just give pass result",default = 0, type="int")
    parser.add_option("-u", "--subframe", action="store", help="subframe number",default = -1, type="int")
    '''
    (options, args) = parser.parse_args()
    #print options,args
    #tv = comparer.getMecacoreVector(options.case,options.tf,options.blk,options.point,options.ant)
    backupDbAuto(options.name, options.targetDir, options.password, options.user)
        
        
        
    
if __name__ == '__main__':
    main()
