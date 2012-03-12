import archiverV2 as archiver
import libSys
#import localLibs.localLibs
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.fileTools as fileTools
import localLibs.collection.fileSystem.fileSystemCollection as fsCollection
import shutil
import os
#from stat import *
import wwjufsdatabase.libs.utils.simplejson as json
import desktopApp.lib.compress.zipClass as zipClass
import archiveStorageBase as archiveStorageBase
import zipStorage as zipStorage
import encryptionStorageBase as encryptionStorageBase

MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024
        
class zipDecStorage(zipStorage.zipStorage):
    def __init__(self, srcRoot, storageRoot, stateStoragePath = 'd:/state.txt', 
                        tmpStorageRoot = 'd:/tmp/removeAfterComplete', decCopier = encryptionStorageBase.arc4DecSimpleCopier('defaultPass')):
        misc.ensureDir(tmpStorageRoot)
        misc.ensureDir(storageRoot)
        zipStorage.zipStorage.__init__(self, srcRoot, storageRoot, stateStoragePath)
        self.tmpStorageRoot = transform.transformDirToInternal(tmpStorageRoot)
        self.decCopier = decCopier

    def store(self, element):
        #print 'storing....'
        targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.tmpStorageRoot, '.zip'))
        print 'copying "%s" to "%s"'%(self.curArchiveName, targetPath)
        self.decCopier.copy(self.curArchiveName, targetPath)
        
        ############################
        #Extract zip file
        ############################
        zf = zipClass.ZFile(targetPath, 'r')
        for i in zf.list():
            targetFullPath = os.path.join(self.storageRoot, i)
            if os.path.exists(targetFullPath):
                print 'file exists:', targetFullPath
            else:
                #print 'extracting file:', targetFullPath
                zf.extract(i, self.storageRoot)
                ############################
                #Do not need to update the source file (encrypted zip file)'s modified time as the archiver will update it
                #But need to update the extracted file's modified time
                ############################
                targetFullPath = os.join(self.storageRoot, i)
                self.config[targetFullPath] = os.stat(targetFullPath).st_mtime
        
        ############################
        #Remove the zip file
        ############################



    
if __name__ == "__main__":
    src = archiveStorageBase.folder('d:/tmp/test')
    ar = archiver.archiverInterface()
    s = zipEncStorage('d:/tmp/test', 'd:/tmp/target', 'd:/state.txt')
    ar.archive(src, s)
    s.saveState()
    