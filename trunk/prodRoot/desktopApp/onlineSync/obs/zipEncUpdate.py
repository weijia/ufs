import localLibSys
import localLibs.localTasks.localTaskInterfacesV2 as taskInterface

class encSyncTask(taskInterface.localTaskBase):
    def process(self):
        '''
        Callback that sub-class should do processing in this method
        '''
        parser = OptionParser()
        parser.add_option("-s", "--sourceDir", action="store",help="copy from which directory")
        parser.add_option("-p", "--encryptionPass", action="store",help="encryption password")
        parser.add_option("-t", "--targetDir", action="store", help="target directory")
        parser.add_option("-c", "--configPath", action="store", help="path for the config file")
        (options, args) = parser.parse_args()
            
        misc.ensureDir(options.targetDir)
        s = zipEncStorage(options.sourceDir, options.targetDir, options.configPath, 
                encCopier = encryptionStorageBase.arc4EncSimpleCopier(options.encryptionPass))
        ar.archive(src, s)
        s.saveState()

        ar = archiver.archiverInterface()

        src = archiveStorageBase.folder(options.sourceDir)

        self.s = encryptionStorageBase.encryptionStorageBase(options.sourceDir, 
            options.targetDir, stateStoragePath = options.configPath, 
            encCopier = encryptionStorageBase.arc4EncSimpleCopier(options.encryptionPass))
        self.ar.archive(src, s)

    def saveState(self):
        '''
        Callback that sub-class should save state in this method
        '''
        s.saveState()

if __name__ == "__main__":
    import sys
    #print sys.argv[0:]
    encSyncTask(sys.argv[0:])