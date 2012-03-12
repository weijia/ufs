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

        
class extractedZipStorage(archiveStorageBase.plainArchiveStorage):
    '''
    self.storageRoot contains the target path
    '''
    def store(self, element):
        #print 'storing....'
        fullPath = transform.transformDirToInternal(element.getAbsPath())
        zf = zipClass.ZFile(fullPath, 'r')
        for i in zf.list():
            targetPath = os.path.join(self.storageRoot, i)
            if os.path.exists(targetPath):
                print 'file exists:', targetPath
            else:
                #print 'extracting file:', targetPath
                zf.extract(i, self.storageRoot)

if __name__ == "__main__":
    src = archiveStorageBase.folder('d:/tmp/test')
    ar = archiver.archiverInterface()
    s = zipStorage('d:/tmp/test', 'd:/tmp/target')
    ar.archive(src, s)
    s.saveState()
    