import archiver as archiver
import libSys
#import localLibs.localLibs
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.misc as misc
import localLibs.collection.fileSystem.fileSystemCollection as fsCollection
import shutil
import os
#from stat import *
import wwjufsdatabase.libs.utils.simplejson as json


class folder(fsCollection.fileSystemCollection, archiver.archivableItemInterface, archiver.archivableContainerInterface):
    '''
    archivable objects shall indicate if it is an container
    '''
    def __init__(self, fullPath, folderOnly = False):
        if not os.path.exists(fullPath):
            raise pathNotExist()
        self.fullPath = transform.transformDirToInternal(fullPath)
        #print self.fullPath
        self.folderOnly = folderOnly
        #print 'folder only:', self.folderOnly
    def isContainer(self) :
        return os.path.isdir(self.fullPath)
    def getAbsPath(self):
        return self.fullPath
    def child(self, childId):
        #print 'returnning child', os.path.join(self.fullPath, childId)
        return folder(os.path.join(self.fullPath, childId))


        
        
class plainArchiveStorage(archiver.archiveStorageInterface):
    def __init__(self, srcRoot, storageRoot, stateStoragePath = 'd:/state.txt'):
        print srcRoot
        self.srcRoot = transform.transformDirToInternal(srcRoot)
        self.storageRoot = transform.transformDirToInternal(storageRoot)
        self.stateStoragePath = stateStoragePath
        try:
            f = open(self.stateStoragePath,'r')
            self.config = json.load(f)
            f.close()
        except IOError:
            self.config = {}
        #print 'storage root:', self.storageRoot
    '''
    def contains(self, element):
        relPath = element.getAbsPath().replace(self.srcRoot+'/', '')
        targetPath = os.path.join(self.storageRoot, relPath)
        #print 'checking:',relPath, targetPath
        return os.path.exists(targetPath)
    '''
    def store(self, element):
        #print 'storing....'
        relPath = element.getAbsPath().replace(self.srcRoot+'/', '')
        targetPath = transform.transformDirToInternal(os.path.join(self.storageRoot, relPath))
        #dirPath = os.path.dirname(targetPath)
        if not os.path.exists(targetPath):
            #print 'copying "%s" to "%s"'%(relPath, targetPath)
            shutil.copy(element.getAbsPath(), targetPath)
            
            
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
    src = folder('d:/tmp/test')
    ar = archiver.archiverInterface()
    s = plainArchiveStorage('d:/tmp/test', 'd:/tmp/target')
    ar.archive(src, s)
    s.saveState()
    