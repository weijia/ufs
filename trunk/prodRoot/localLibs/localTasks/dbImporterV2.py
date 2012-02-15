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
import dbExporterV3 as listEncryptor
import libs.user.userManagerV2 as userMan
#import libs.ufsDb.multiAccountDbSys as dbSys
import libs.services.servicesV2 as service
import wwjufsdatabase.libs.shove.encryptedListShove as xorEnc

def importDb(input, username, targetPasswd, password = None):
    dbSysInst = dbSys.dbSysSmart()
    sf = open(input, 'r')
    package = json.load(sf)
    en = enc.encryptorBase64Out(password)
    l = package["add"]
    if (password is None) and package.has_key("encPass"):
        print 'need password for importing'
        return
    if (not (password is None)):
        if unicode(str(md5.new(password).hexdigest())) != package["encPass"]:
            print 'pass not match:', unicode(str(md5.new(password+package["time-duration"]).hexdigest())), package["encPass"]
            return
        else:
            l = listEncryptor.dictListDecryptor(l, en)
    sysUser = service.ufsUser(u'system.user', u'system.pass')
    if userMan.userManager().verifyPasswd(username, targetPasswd, dbSys.dbSysSmart(sysUser).getDb("passwdDb")):
        print 'importing'
        l = listEncryptor.dictListEncryptor(l, xorEnc.encryptorTxtOut(targetPasswd))
        #print l
        l = listEncryptor.setUser(l, username)
        #print l
        dbSysInst.importDb(l)
    
def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", help="database import full path",default = 'D:\\tmp\\backup\\backup.json')
    parser.add_option("-p", "--password", action="store",help="password for target output",default = None)
    parser.add_option("-t", "--target", action="store",help="password for database",default = None)
    parser.add_option("-u", "--username", action="store",help="username for database",default = None)

    (options, args) = parser.parse_args()
    importDb(options.input, unicode(options.username), options.target, options.password)
    
if __name__ == '__main__':
    main()
