import localLibSys

import wwjufsdatabase.libs.ufsDb.ufsDbSingleUser as dbSys
import wwjufsdatabase.libs.utils.simplejson as json
from optparse import OptionParser
import wwjufsdatabase.libs.tag.sessionBase as sessionBase
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.configurationTools as cfg
import os
import wwjufsdatabase.libs.encryption.arc4Encryptor as enc
import md5
import wwjufsdatabase.libs.shove.encryptedListShove as xorEnc
import uuid
import re


encryptedKeys = ["key", "value"]
    
def dictListDecryptor(dictList, encryptor = xorEnc.encryptorTxtOut('simpleKey')):
    #e = enc.encryptor()
    res = []
    for i in dictList:
        resV = {}
        for j in i:
            if j in encryptedKeys:
                #Need decryption
                try:
                    resV[j] = encryptor.de(i[j])
                except ValueError:
                    continue
                #print encryptor.de(i[j]).encode('gbk')
            else:
                resV[j] = i[j]
        #print resV
        res.append(resV)
    return res

def dictListEncryptor(dictList, encryptor = xorEnc.encryptorTxtOut('simpleKey')):
    #e = enc.encryptor()
    res = []
    for i in dictList:
        resV = {}
        for j in i:
            if j in encryptedKeys:
                #Need decryption
                resV[j] = encryptor.en(i[j])
                #print encryptor.de(i[j]).encode('gbk')
            else:
                resV[j] = i[j]
        #print resV
        res.append(resV)
    return res
    
def setUser(dictList, user):
    #e = enc.encryptor()
    res = []
    for i in dictList:
        resV = {}
        for j in i:
            if j in [u'user']:
                #Need decryption
                resV[j] = user
                #print encryptor.de(i[j]).encode('gbk')
            else:
                resV[j] = i[j]
        #print resV
        res.append(resV)
    return res

    
def findLastTimestamp(targetDir, hostname):
    '''
    Backup files will has the name as "host-name_time.start_time.end.xxx.json"
    '''
    lastTime = 0
    for i in os.listdir(targetDir):
        m = re.search("([^_]+)_(\d+(\.\d+)?)-(\d+(\.\d+)?).+", i)
        #print i
        if m is None:
            print 'no match'
            continue
        startTime = m.group(2)
        endTime = m.group(4)
        #print m.group(0), m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        if m.group(1) != hostname:
            continue
        #print startTime, endTime
        floatEndTime = float(endTime)
        if lastTime < floatEndTime:
            lastTime = floatEndTime
    return lastTime
    
def exportDb(targetDir, password = None, hostname = None):
    dbSysInst = dbSys.dbSysSmart()
    startTime = findLastTimestamp(targetDir, hostname)
    endTime = dbSysInst.getTimeStamp()
    finalRes = dbSysInst.exportDb(startTime, endTime, hostname)
    if len(finalRes) == 0:
        print 'no update need to be exported'
        return
    finalRes = dictListDecryptor(finalRes)
    timeStampName = "%s-%s"%(startTime, endTime)
    package = {"backup-id": unicode(str(uuid.uuid4())), "time-duration":timeStampName}
    if password is None:
        package["add"] = finalRes
        fullname = '%s_%s.noenc.json'%(hostname, timeStampName)
    else:
        fullname = '%s_%s.json'%(hostname, timeStampName)
        en = enc.encryptorBase64Out(password)
        finalRes = dictListEncryptor(finalRes, en)
        package["encPass"] = unicode(str(md5.new(password+timeStampName).hexdigest()))
        package["add"] = finalRes
    targetFullPath = os.path.join(targetDir, fullname)
    s = json.dumps(package, sort_keys=True, indent=4)
    #s = json.dumps(package)
    f = open(targetFullPath,'w')
    f.write(s)
    f.close()


def main():
    c = cfg.configuration()
    defaultTarget = os.path.join(c.get('host.root', 'd:/tmp/fileman'), 'backup/sync')
    parser = OptionParser()
    #parser.add_option("-u", "--user", action="store",help="username for the database system",default = None)
    parser.add_option("-i", "--ignore", action="store_true",help="no password for exported db", default = False)
    parser.add_option("-t", "--targetDir", action="store", help="database backup target directory",default = defaultTarget)
    parser.add_option("-o", "--hostname", action="store", help="database name for backup",default = None)
    #parser.add_option("-n", "--name", action="store", help="database name for backup",default = None)
    #parser.add_option("-s", "--show", action="store", help="print time stamp of last backup",default = None)
    #parser.add_option("-r", "--reset", action="store", help="reset backup timestamp",default = None)
    
    (options, args) = parser.parse_args()
    if options.hostname is None:
        hostname = c.get('host.hostname','q19420-01')
    else:
        hostname = options.hostname
    if options.ignore:
        print 'Warning!!!.....No password for the db'
        password = None
    else:
        if 0 == len(args):
            print 'Password is rquired, please enter the password following the command'
            #print args
            return
        password = args[0]
    exportDb(options.targetDir, password, hostname)
        
        
    
if __name__ == '__main__':
    main()
