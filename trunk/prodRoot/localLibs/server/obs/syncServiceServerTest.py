import xmlrpclib
import localLibSys
import wwjufsdatabase.libs.utils.transform as transform
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8806/xmlrpc")

    syncFolderCollectionId = 'uuid://088b222c-d86c-4a59-8084-3cfc9aa3fcc7'
    logCollectionId = 'uuid://c6e1e1a8-8e18-42d5-b1e1-0a24938048d'
    taskName = "test task112"
    gAppUuid = 'fa38c942-15ed-4fa8-a0d2-a7ab013e5c0b'

    # Print list of available methods
    
    print proxy.createSync(taskName, gAppUuid, "D:/tmp/fileman/target/data", "D:/tmp/fileman/target/backup",
                                    syncFolderCollectionId,
                                    transform.transformDirToInternal("D:\\tmp\\fileman\\data\\encZip"), 
                                    logCollectionId, "D:/tmp/dbOrientTest", sys.argv[1])
                                    
    
    '''
    print proxy.startSync()
    '''