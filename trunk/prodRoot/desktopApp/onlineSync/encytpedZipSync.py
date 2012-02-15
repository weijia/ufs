import localLibSys
#import localLibs.localTasks.localTaskInterfacesV2 as taskInterface
import os
from optparse import OptionParser
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform
import encZipStorageV2 as encZipStorage
import configDict as configDict
import folderStorageV3 as folderStorage

class encSyncTask:
    def __init__(self, taskName):
        #print taskName
        #taskInterface.localTaskBase.__init__(self, taskName)
        pass
        
    def initParam(self, zipDir, folderDir, workingDir, encryptionPass, direction):
        #################################
        #Make dir if not exist
        #################################
        misc.ensureDir(zipDir)
        misc.ensureDir(workingDir)
        misc.ensureDir(folderDir)
        self.configPath = os.path.join(workingDir, 'workingState.txt')
        self.backupPath = os.path.join(workingDir, 'backup')
        misc.ensureDir(self.backupPath)
        self.tmpStorageRoot = transform.transformDirToInternal(os.path.join(workingDir, 'working'))
        self.config = configDict.configFileDict(self.configPath, {"zipStorageState":{}, "folderState":{}})

        #################################
        #Create source storage
        #################################
        
        self.storage1 = encZipStorage.encZipStorage(self.config["zipStorageState"], 
                self.tmpStorageRoot, zipDir, encryptionPass)
        #################################
        #Create target storage
        #################################
        self.storage2 = folderStorage.folderStorage(self.config["folderState"], 
                folderDir, self.backupPath)
        
        if direction == "extract":
            self.srcStorage = self.storage1
            self.dstStorage = self.storage2
        else:
            self.srcStorage = self.storage2
            self.dstStorage = self.storage1

    def run(self):
        itemGenerator = self.srcStorage.getNextUpdatedItem()
        for item in itemGenerator:
            #Need to update target storage, so the updated items in target storage will not be sync to src when
            #a reverse sync is performed, this should be done in store operation
            self.dstStorage.store(item)
            #Update src storage sync state so the updated items will not be sync again
            self.srcStorage.update(item)
        self.config["folderState"] = self.storage2.getState()
        self.config["zipStorageState"] = self.storage1.getState()
        self.saveState()

    def saveState(self):
        '''
        Callback that sub-class should save state in this method
        '''
        self.config.store()


if __name__ == "__main__":
    import sys
    #print sys.argv[0:]
    e = encSyncTask(str(sys.argv[0:]))
    parser = OptionParser()
    parser.add_option("-f", "--folder", action="store",help="copy from which directory", default="d:/tmp/test/source")
    parser.add_option("-p", "--encryptionPass", action="store",help="encryption password")
    parser.add_option("-z", "--zipDir", action="store", help="target directory", default="d:/tmp/test/zip")
    #parser.add_option("-c", "--configPath", action="store", help="path for the config file")
    parser.add_option("-w", "--workingPath", action="store", help="path for temp file", default="d:/tmp/test/working")
    #parser.add_option("-b", "--backupPath", action="store", help="path for backup files")
    parser.add_option("-d", "--direction", action="store", help="syncDirection", default="sync")
    parser.add_option("-t", "--test", action="store", help="syncDirection", default="test")
    (options, args) = parser.parse_args()
    if options.test == "test":
        passwd = "testPass"
    else:
        passwd = options.encryptionPass
    e.initParam(options.zipDir, options.folder, options.workingPath, passwd, options.direction)
    e.run()