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
        
class zipEncStorage(zipStorage.zipStorage):
    def __init__(self, srcRoot, storageRoot, stateStoragePath = 'd:/state.txt', 
                        tmpStorageRoot = 'd:/tmp/removeAfterComplete', encCopier = encryptionStorageBase.arc4EncSimpleCopier('defaultPass')):
        misc.ensureDir(tmpStorageRoot)
        misc.ensureDir(storageRoot)
        zipStorage.zipStorage.__init__(self, srcRoot, storageRoot, stateStoragePath)
        self.tmpStorageRoot = transform.transformDirToInternal(tmpStorageRoot)
        self.encCopier = encCopier
        self.createNewZip()
        
    def createNewZip(self):
        ####################
        #Create new zip file
        ####################
        self.curArchiveName = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.tmpStorageRoot, '.zip'))
        self.curArchive = zipClass.ZFile(self.curArchiveName, 'w')
        self.curArchivedSize = 0
    def encZip(self):
        ############################
        #Encrypt the zip file
        ############################
        targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.storageRoot, '.enc'))
        print 'copying "%s" to "%s"'%(self.curArchiveName, targetPath)
        self.encCopier.copy(self.curArchiveName, targetPath)
        ############################
        #TODO: Remove the zip file
        ############################

    def store(self, element):
        #print 'storing....'
        fullPath = transform.transformDirToInternal(element.getAbsPath())
        relPath = fullPath.replace(self.srcRoot, '')
        if (self.curArchivedSize > MAX_SINGLE_ARCHIVE_SIZE):
            self.encZip()
            self.createNewZip()

        #print 'copying "%s" to "%s"'%(fullPath, relPath)
        self.curArchive.addfile(unicode(fullPath).encode('gbk'), unicode(relPath).encode('gbk'))
        self.curArchivedSize += os.stat(fullPath).st_size
        #print 'archived:%d'%self.curArchivedSize
    def saveState(self):
        self.encZip()
        zipStorage.zipStorage.saveState(self)

    
if __name__ == "__main__":
    src = archiveStorageBase.folder('d:/tmp/test')
    ar = archiver.archiverInterface()
    s = zipEncStorage('d:/tmp/test', 'd:/tmp/target', 'd:/state.txt')
    ar.archive(src, s)
    s.saveState()
    