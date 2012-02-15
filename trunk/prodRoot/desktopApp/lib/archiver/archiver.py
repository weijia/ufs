'''
Use case:
Sync files in 2 directory
Sync files in 2 directory, encrypt them in the same time
Achive files from 1 directory to anther, with encryption and compress
Save files to mail box
Upload files from local to online storage, mailbox, doc space etc.
Download files from online storage
Requirement:
App shall record sync state
Solutions:
According to date: record the last sync date, update files after the last sync
     List all files created later than the recorded time.
        Update the target files according to the list.
        If archive, use new date as the archive name
        If copy, and same name exist, rename the old file with time stamp and copy the new one
According to a list: record all updated files.
    List all files that is not in the updated list
    If archive, use the new date as the archive name
    If copy, and same name exist, rename the old file with time stamp and copy the new one
According to a list of checksum: record all updated files with checksum.
    List all files that is not updated with different checksum.
    If archive, use the new date as the archive name
    If copy, and same name exist, rename the old file with time stamp and copy the new one
Design:
Classes:
    archiver: provide an algrithm for the above solutions
    archivable: provide a storage that can provide file list
    archiveStorage: provide a storage to contain archived data
'''
class archivableBaseInterface:
    '''
    archivable objects shall indicate if it is an container
    '''
    def isContainer(self) :
        pass
    def getAbsPath(self):
        pass
    def getRalative(self, root):
        pass
        
class archivableContainerInterface(archivableBaseInterface):
    '''
    Container should have these functions
    '''
    def getRange(self, start, cnt):
        '''
        Return a collection of items, just like normal collection
        '''
        pass
    def child(self, childId):
        '''
        Return a child archivableItem
        '''
        pass
        
class archivableItemInterface(archivableBaseInterface):
    def getDataId(self):
        pass
    def readData(self, dataId):
        pass
    def getTimestamp(self):
        pass
        
class  archiveStorageInterface:
    def contains(self, element):
        pass
    def store(self, element):
        pass
        
class archiverInterface:
    '''
     provide an algorithm for the above solutions
    '''
    def archive(self, archivableInst, archiveStorageInst):
        '''
        Get a list of updated files and archive them, archivableInst should have archivableIterface, archiveStorageInst should have archiveStorageInterface
        '''
        index = 0
        processLen = 50
        #print archivableInst
        if not archiveStorageInst.updated(archivableInst):
            #print 'skipping: ',archivableInst.getAbsPath()
            #return
            pass
        while True:
            res = archivableInst.getRange(index, processLen)
            #print index, processLen, res
            #return
            index += processLen
            #print res
            if 0 == len(res):
                break
            for i in res:
                #print 'processing:', i.encode('gbk', 'replace')
                if archivableInst.child(i).isContainer():
                    self.archive(archivableInst.child(i), archiveStorageInst)
                if not archiveStorageInst.contains(archivableInst.child(i)):
                    archiveStorageInst.store(archivableInst.child(i))
        archiveStorageInst.updated(archivableInst, True)
        
    def sync(self):
        '''
        TBD
        '''
        pass
