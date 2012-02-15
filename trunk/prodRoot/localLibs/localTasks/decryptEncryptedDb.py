from optparse import OptionParser
import dbExporterV3
import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.encryption.arc4Encryptor as enc
import md5
def decryptBackup(sourceFullPath, target, password = None):
    sf = open(sourceFullPath, 'r')
    l = json.load(sf)
    if l.has_key("encPass"):
        if password is None:
            print 'need password'
            return
        else:
            en = enc.encryptorBase64Out(password)
            if str(md5.new(password+l["time-duration"]).hexdigest()) != l["encPass"]:
                print 'pass not match:', str(md5.new(password+l["time-duration"]).hexdigest()), l["encPass"]
                return
            res = dbExporterV3.dictListDecryptor(l["add"], en)
    else:
        res = l["add"]
    l["add"] = res
    del l["encPass"]
    s = json.dumps(l, sort_keys=True, indent=4)
    f = open(target,'w')
    f.write(s)
    f.close()

def main():
    parser = OptionParser()
    #parser.add_option("-u", "--user", action="store",help="username for the database system",default = None)
    parser.add_option("-p", "--password", action="store",help="password for target output",default = None)
    parser.add_option("-t", "--target", action="store", help="database backup target directory",default = 'd:/tmp/fileman/backup/sync/db.decrypted.json')
    parser.add_option("-s", "--source", action="store", help="database backup source directory",default = 'D:\\tmp\\backup\\backup.json')
    #parser.add_option("-n", "--name", action="store", help="database name for backup",default = None)

    (options, args) = parser.parse_args()
    #print options,args
    #tv = comparer.getMecacoreVector(options.case,options.tf,options.blk,options.point,options.ant)
    decryptBackup(options.source, options.target, options.password)

        
        
    
if __name__ == '__main__':
    main()
