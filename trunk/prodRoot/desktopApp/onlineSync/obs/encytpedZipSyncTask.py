import localLibSys
import localLibs.localTasks.localTaskInterfacesV2 as taskInterface
import os
from optparse import OptionParser
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform
import encZipStorage as encZipStorage
import configDict as configDict
import folderStorage as folderStorage

class encSyncTask(taskInterface.localTaskBase):
    def __init__(self, taskName):
        #print taskName
        taskInterface.localTaskBase.__init__(self, taskName)
        parser = OptionParser()

        parser.add_option("-f", "--folder", action="store",help="copy from which directory")
        parser.add_option("-p", "--encryptionPass", action="store",help="encryption password")
        parser.add_option("-z", "--zipDir", action="store", help="target directory")
        parser.add_option("-c", "--configPath", action="store", help="path for the config file")
        parser.add_option("-w", "--workingPath", action="store", help="path for temp file")
        parser.add_option("-b", "--backupPath", action="store", help="path for backup files")
        parser.add_option("-d", "--direction", action="store", help="syncDirection")
        (options, args) = parser.parse_args()
        self.options = options
        self.configPath = options.configPath
        self.config = configDict.configFileDict(options.configPath, {"zipStorageState":{}, "folderState":{}})
        self.tmpStorageRoot = transform.transformDirToInternal(options.workingPath)
        
        #################################
        #Make dir if not exist
        #################################
        misc.ensureDir(options.zipDir)
        misc.ensureDir(self.tmpStorageRoot)
        misc.ensureDir(self.options.backupPath)
        misc.ensureDir(self.options.folder)
        
        #################################
        #Create source storage
        #################################
        
        self.storage1 = encZipStorage.encZipStorage(self.config["zipStorageState"], 
                self.tmpStorageRoot, self.options.zipDir, self.options.encryptionPass)
        #################################
        #Create target storage
        #################################
        self.storage2 = folderStorage.folderStorage(self.config["folderState"], 
                self.options.folder, self.options.backupPath)
        
        if self.options.direction == "extract":
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
            break
            if not self.delayRunning():
                break
        self.config["encState"] = self.storage2.getState()
        self.config["extractState"] = self.storage1.getState()
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
    e.run()