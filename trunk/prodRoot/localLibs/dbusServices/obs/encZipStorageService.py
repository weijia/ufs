import localLibSys
import localLibs.dbusServices.dbusServiceBase as dbusServiceBase
import localLibs.collection.objectDatabase as objectDatabase
import desktopApp.onlineSync.encZipStorageV3 as encZipStorage
import dbus

import os
from optparse import OptionParser
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.onlineSync.encZipStorageV3 as encZipStorage
import desktopApp.onlineSync.configDict as configDict
import desktopApp.onlineSync.folderStorageV3 as folderStorage

INTERFACE_NAME = 'com.wwjufsdatabase.encZipStorageService'


class encZipStorageService(dbusServiceBase.dbusServiceBase):
    def __init__(self, sessionBus, objectPath):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        parser = OptionParser()
        parser.add_option("-p", "--encryptionPass", action="store",help="encryption password", default="defaultPass")
        parser.add_option("-z", "--zipDir", action="store", help="target directory", default="d:/tmp/sync/encZipRoot/zip")
        parser.add_option("-w", "--workingPath", action="store", help="path for temp file", default="D:\\tmp\\sync\\encZipRoot\\tmp")
        parser.add_option("-t", "--test", action="store", help="syncDirection", default="test")
        (options, args) = parser.parse_args()
        if options.test == "test":
            passwd = "testPass"
        else:
            passwd = options.encryptionPass
        self.initParam(options.zipDir, options.workingPath, passwd)

        
    def initParam(self, zipDir, workingDir, encryptionPass):
        #################################
        #Make dir if not exist
        #################################
        misc.ensureDir(zipDir)
        misc.ensureDir(workingDir)
        #misc.ensureDir(folderDir)
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
                'd:/tmp/sync/encZipRoot/folder', self.backupPath)
        
        if False:#direction == "extract":
            self.srcStorage = self.storage1
            self.dstStorage = self.storage2
        else:
            self.srcStorage = self.storage2
            self.dstStorage = self.storage1

    '''
    def run(self):
        itemGenerator = self.srcStorage.getNextUpdatedItem()
        for item in itemGenerator:
            #Need to update target storage, so the updated items in target storage will not be sync to src when
            #a reverse sync is performed, this should be done in store operation
            self.dstStorage.store(item)
            #Update src storage sync state so the updated items will not be sync again
            self.srcStorage.update(item)
    '''

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='')
    def store(self, itemFullPath):
        '''
        Add new item or updated item to collection, if changeNotification is 
        True, the item will not be submitted until certain time period passed
        '''
        print itemFullPath
        #Generate the item
        ufsObj = getFsObj(u'file:///'+itemFullPath)
        self.storage.store(ufsObj)
        #Update src storage sync state so the updated items will not be sync again
        self.srcStorage.update(ufsObj)
        
    def exitServiceCallback(self):
        self.config["folderState"] = self.storage2.getState()
        self.config["zipStorageState"] = self.storage1.getState()
        self.saveState()
    def saveState(self):
        '''
        Callback that sub-class should save state in this method
        '''
        self.config.store()


'''
if __name__ == "__main__":
    import sys
    #print sys.argv[0:]
    e = encSyncTask(str(sys.argv[0:]))
    e.run()
'''