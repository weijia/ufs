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

MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024
        
class zipStorage(archiveStorageBase.plainArchiveStorage):
    def __init__(self, srcRoot, storageRoot, stateStoragePath = 'd:/state.txt'):
        #print 'src root:',srcRoot
        self.srcRoot = transform.transformDirToInternal(srcRoot)
        self.storageRoot = transform.transformDirToInternal(storageRoot)
        #print self.srcRoot
        #print self.storageRoot
        self.stateStoragePath = stateStoragePath
        try:
            f = open(self.stateStoragePath,'r')
            self.config = json.load(f)
            f.close()
        except IOError:
            self.config = {}
        #print 'storage root:', self.storageRoot
        self.curArchivedSize = 0
        self.curArchive = None

    def store(self, element):
        #print 'storing....'
        fullPath = transform.transformDirToInternal(element.getAbsPath())
        relPath = fullPath.replace(self.srcRoot, '')
        if (self.curArchive is None) or (self.curArchivedSize > MAX_SINGLE_ARCHIVE_SIZE):
            self.curArchiveName = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.storageRoot, '.zip'))
            self.curArchive = zipClass.ZFile(self.curArchiveName, 'w')
            self.curArchivedSize = 0
        #print 'copying "%s" to "%s"'%(fullPath, relPath)
        self.curArchive.addfile(unicode(fullPath).encode('gbk'), unicode(relPath).encode('gbk'))
        self.curArchivedSize += os.stat(fullPath).st_size
        #print 'archived:%d'%self.curArchivedSize
            
    def updated(self, element):
        fullPath = transform.transformDirToInternal(element.getAbsPath())
        relPath = fullPath.replace(self.srcRoot, '')
        #print 'checking:',relPath, fullPath
        try:
            return not (self.config[fullPath] == os.stat(element.getAbsPath()).st_mtime)
        except KeyError:
            return True
    def updateModTime(self, element):
        fullPath = transform.transformDirToInternal(element.getAbsPath())
        relPath = fullPath.replace(self.srcRoot, '')
        self.config[fullPath] = os.stat(fullPath).st_mtime
        #print 'update state for:',targetPath.encode('gbk', 'replace')
    def saveState(self):
        s = json.dumps(self.config, sort_keys=True, indent=4)
        #s = json.dumps(package)
        f = open(self.stateStoragePath,'w')
        f.write(s)
        f.close()

if __name__ == "__main__":
    src = archiveStorageBase.folder('d:/tmp/test')
    ar = archiver.archiverInterface()
    s = zipStorage('d:/tmp/test', 'd:/tmp/target')
    ar.archive(src, s)
    s.saveState()
    