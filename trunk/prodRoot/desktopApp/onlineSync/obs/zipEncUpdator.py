import localLibSys
import localLibs.localTasks.localTaskInterfacesV2 as taskInterface
import os
from optparse import OptionParser
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
import wwjufsdatabase.libs.utils.fileTools as fileTools
import desktopApp.lib.compress.zipClass as zipClass
#import wwjufsdatabase.libs.utils.simplejson as json
import configDict as configDict

MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024


def dirTreeGenerator(rootDir):
    for i in os.walk(rootDir):
        #print i
        for j in i[2]:
            yield transform.transformDirToInternal(os.path.join(i[0], j))


class encSyncTask(taskInterface.localTaskBase):
    def __init__(self, taskName):
        #print taskName
        taskInterface.localTaskBase.__init__(self, taskName)
        parser = OptionParser()

        parser.add_option("-s", "--sourceDir", action="store",help="copy from which directory")
        parser.add_option("-p", "--encryptionPass", action="store",help="encryption password")
        parser.add_option("-t", "--targetDir", action="store", help="target directory")
        parser.add_option("-c", "--configPath", action="store", help="path for the config file")
        parser.add_option("-w", "--workingPath", action="store", help="path for temp file")
        (options, args) = parser.parse_args()
        self.options = options
        self.configPath = options.configPath
        self.config = configDict.configFileDict(options.configPath, {'timestamp':{}})
        misc.ensureDir(options.targetDir)
        self.objList = dirTreeGenerator(self.options.sourceDir)
        self.tmpStorageRoot = transform.transformDirToInternal(options.workingPath)
        misc.ensureDir(self.tmpStorageRoot)
        misc.ensureDir(self.options.targetDir)
        self.encCopier = encryptionStorageBase.arc4DecSimpleCopier(options.encryptionPass)
        #self.createNewZip()
        self.curArchive = None

    def process(self):
        '''
        Callback that sub-class should do processing in this method
        '''
        try:
            nextItem = self.objList.next()
            self.handleItem(nextItem)
        except StopIteration:
            #Return True to stop processing
            return True
        return False
        
    def createNewZip(self):
        ####################
        #Create new zip file
        ####################
        self.curArchiveName = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.options.workingPath, '.zip'))
        self.curArchive = zipClass.ZFile(self.curArchiveName, 'w')
        self.curArchivedSize = 0
        
    def encZip(self):
        if self.curArchive is None:
            return
        ############################
        #Encrypt the zip file
        ############################
        targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.options.targetDir, '.enc'))
        print 'copying "%s" to "%s"'%(self.curArchiveName, targetPath)
        self.encCopier.copy(self.curArchiveName, targetPath)
        ############################
        #TODO: Remove the zip file
        ############################

    def handleItem(self, nextItem):
        if self.updated(nextItem):
            if self.curArchive is None:
                self.createNewZip()
            fullPath = transform.transformDirToInternal(nextItem)
            relPath = fullPath.replace(self.options.sourceDir, '')
            if (self.curArchivedSize > MAX_SINGLE_ARCHIVE_SIZE):
                self.encZip()
                self.createNewZip()
            ##############################
            #TODO: Create an index for the target zip file
            ##############################
            #print 'copying "%s" to "%s"'%(fullPath, relPath)
            self.curArchive.addfile(unicode(fullPath).encode('gbk'), unicode(relPath).encode('gbk'))
            self.curArchivedSize += os.stat(fullPath).st_size
            #print 'archived:%d'%self.curArchivedSize
            self.updateModTime(fullPath)
        
    def updated(self, fullPath):
        fullPath = transform.transformDirToInternal(fullPath)
        try:
            return not (self.config['timestamp'][fullPath] == os.stat(fullPath).st_mtime)
        except KeyError:
            return True
            
    def updateModTime(self, fullPath):
        fullPath = transform.transformDirToInternal(fullPath)
        self.config['timestamp'][fullPath] = os.stat(fullPath).st_mtime
        #print 'update state for:',fullPath.encode('gbk', 'replace')

    def saveState(self):
        '''
        Callback that sub-class should save state in this method
        '''
        self.encZip()
        self.config.store()


if __name__ == "__main__":
    import sys
    #print sys.argv[0:]
    e = encSyncTask(str(sys.argv[0:]))
    e.run()