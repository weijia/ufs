from ufsTreeItem import ufsTreeItemBase
import localLibSys
import desktopApp.libs.windows.netdisk.driver_mapping as driverMapping
import libs.localDb.dictShoveDb as dictShoveDb

class smbTreeItem(ufsTreeItemBase):
    def __init__(self, itemUrl):
        """
        ufsUrl = smb://mybook:pass@192.168.1.102/
        itemUrl = mybook:pass@192.168.1.102/
        """
        db = dictShoveDb.getDb("smbTmpInfo")
        userPass, server = itemUrl.split("@", 2)
        user, passwd = userPass.split(":",2)
        server = "\\\\"+server.replace("/",'\\')
        try:
            self.driver = db[server]
        except KeyError:
            print 'not mapped'
            #Not mapped, map it
            #find an empty driver letter
            s = driverMapping.sys_driver_mapping()
            m = s.get_mapping()
            i = 'z'
            while ord(i)>ord('a'):
                try:
                    a = m[i]
                except KeyError:
                    break
                i = chr(ord(i)-1)
            if ord(i) == ord('a'):
                raise "no driver letter available"
            print 'subst %s, %s'%(i, server)
            s.subst_driver(server, i)
            
            db[server] = i
            self.driver = i
    def getName(self, p):
        pass
        
    def isContainer(self, p):
        '''
        return os.path.isdir(p)
        '''
        pass

    def child(self, fullPath):
        pass


def getUfsTreeItem(itemUrl):
    return smbTreeItem(itemUrl)
    
    
def main():
    s = driverMapping.sys_driver_mapping()
    m = s.get_mapping()
    for i in m:
        print i+":"+s.mapping[i]
    k = getUfsTreeItem("mybook:pass@192.168.1.102/public")
    m = s.get_mapping()
    for i in m:
        print i+":"+s.mapping[i]
     
if __name__ == '__main__':
    main()
