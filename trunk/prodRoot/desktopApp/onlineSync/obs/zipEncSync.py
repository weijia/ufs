import wwjufsdatabase.libs.utils.transform as transform


class storageCollectionItem:
    def getTimestamp(self):
        pass

class storageCollectionInterface:
    def getRange(self, start = 0, cnt = None, timestamp = None):
        pass
    def getTimestamp(self):
        pass

class encZipItemInterface:
    def getRelativePath():
        pass
    def getTimestamp(self):
        pass
    def copyTo(self):
        pass
        
class encZipStorage(storageCollectionInterface):
    def __init__(self, storageRoot, configDict, passwd):
        self.configDict = configDict
    def store(self, obj):
        pass
    def checkModification(self, item):
        relaPath = transform.formatRelativePath(item.getRelativePath())
        self.configDict
        
        
class dirItem:
    def __init__(self, fullPath, rootPath):
        pass
    def getRelativePath():
        pass
    def getTimestamp(self):
        pass
    def copyTo(self):
        pass
        
        
class folderStorage(storageCollectionInterface):
    def __init__(self, storageRoot, configDict):
        self.configDict = configDict
        self.storageRoot = storageRoot
        
    def store(self, item):
        '''
        Copy the item to this storage and update the timestamp of it
        '''
        item.copyTo(self.storageRoot)
        self.recordItemInfo(item)
    '''
    def checkModification(self, item):
        relaPath = transform.formatRelativePath(item.getRelativePath())
        fullPath = os.path.join(self.storageRoot, relaPath)
        try:
            if self.configDict[relaPath] == os.stat(fullPath).st_mtime:
                return False
        except KeyError:
            pass
        return True
    '''
    def recordItemInfo(self, item):
        relaPath = transform.formatRelativePath(item.getRelativePath())
        fullPath = os.path.join(self.storageRoot, relaPath)
        self.configDict[relaPath] = os.stat(fullPath).st_mtime

    def getState(self):
        return self.configDict
    
    def getUpdatedItems(self):
        updatedItemNames = []
        for i in os.walk(self.storageRoot):
            for j in i[2]:
                fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
                try:
                    if self.configDict[fullPath] == os.stat(fullPath).st_mtime:
                        continue
                except KeyError:
                    pass
                    updatedItemNames.append(dirItem(fullPath, self.storageRoot))
        return updatedItemNames

                
        
class syncTask:
    def __init__(self, srcStorage, destStorage, configDict):
        ############################
        #Get local file list and file timestampes
        ############################
        self.srcStorage = srcStorage
        localList = self.storage1.getRange()
        ############################
        #Get recorded local file list and file timestampes
        ############################

        ############################
        #Get remote file list and file timestampes
        ############################
        self.destStorage = destStorage
        remoteList = self.destStorage.getRange()
    def process(self):
        ############################
        #Process the local file list, find the upadted ones
        ############################
        
        #If the file was updated locally
            #If remote storage didn't have this latest item, add it
            #If remote storage has a more newer version, add it?
        
        ############################
        #Process the remotely file list, find the updated ones
        ############################
        
        self.handleItem(self.itemGenerator.next())
        
    def handleItem(self, item, srcStorage, dstStorage)
        #Check the relativePath in srcStorage to see if it was updated in the srcStorage
        dstStorage.store(item)
        #If remote storage has a more newer version, add it?

