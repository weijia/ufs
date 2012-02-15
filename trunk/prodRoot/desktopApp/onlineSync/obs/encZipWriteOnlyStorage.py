import os
import localLibSys

import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import desktopApp.lib.compress.zipClass as zipClass
import folderStorage as folderStorage
import localLibs.localTasks.infoCollector as infoCollector
import wwjufsdatabase.libs.utils.simplejson as json


MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024
'''
class encZipStorageItem(folderStorage.folderStorageItem):
    def __init__(self, rootPath, archivePath, relaPath, extractedPath):
        self.rootPath = transform.transformDirToInternal(rootPath)
        self.relaPath = relaPath
        self.fullPath = transform.transformDirToInternal(extractedPath)
        self.archivePath = transform.transformDirToInternal(archivePath)
        
    #########################################################
    #The following methods are used only for tracking update state
    #########################################################
    def getTimestamp(self):
        return os.stat(self.fullPath).st_mtime
    def getItemId(self):
        return self.getRelaPath()
    #########################################################
    #The following methods are used only for encrypted zip storage
    #########################################################
    def getFullPath(self):
        return self.fullPath
    def getRelaPath(self):
        return self.relaPath
    def getArchivePath(self):
        return archivePath
'''
# class encZipStorageState(folderStorage.folderStorageState):
    # '''
    # def __init__(self, stateDict):
        # self.stateDict = stateDict
    # def updated(self, item):
        # try:
            # if self.stateDict[item.getItemId()] == item.getTimestamp():
                # return False
            # return True
        # except KeyError:
            # return True
    # '''
    # def update(self, item):
        # self.stateDict[item.getItemId()] = {"timestamp": item.getTimestamp(), "fullPath":item.getFullPath(),
            # "headMd5":infoCollector.getHeadContentMd5(item.getFullPath()), "parentZip":item.getArchivePath()}
    # '''
    # def getState(self):
        # return self.stateDict
    # '''
        
def getTimeTuple(seconds):
    t = time.localtime(seconds)
    return (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    
def getTimeInSeconds(timeStructure):
    finalRes = []
    for i in timeStructure:
        finalRes.append(i)
    finalRes.extend([0,0,0])
    return time.mktime(finalRes)

def getEncZipLogFilenameFromEncrypted(encryptedFilePath):
    return encryptedFilePath.replace('.enc', 'enclog')
    
    
'''
{
    "15990197630-SysCfg.xml": {
        "headMd5": "2f13161d7594011b47f99a6878475efe", 
        "parentEncZip": "D:/oldmachine/sys/my-sync/pidgin/data/1311527042.02.enc", 
        "size": 15336, 
        "timestamp": 12345678.1
    }, 
'''
    
class encZipWriteOnlyStorage(folderStorage.storageInterface):
    def __init__(self, lastState, workingDir, zipStorageDir, passwd):
        self.lastState = folderStorage.folderStorageState(lastState)
        #self.selfState = folderStorage.folderStorageState({})
        self.zipContentState = {}
        self.workingDir = workingDir + '/zipfiles'
        self.decryptionWorkingDir = workingDir + '/decrypted'
        self.zipStorageDir = zipStorageDir
        self.passwd = passwd
        self.encCopier = encryptionStorageBase.arc4EncSimpleCopier(passwd)
        self.decCopier = encryptionStorageBase.arc4DecSimpleCopier(passwd)
        
        misc.ensureDir(self.workingDir)
        misc.ensureDir(self.decryptionWorkingDir)
        
        
        ########################################
        #Internal used vars
        ########################################
        self.curArchive = None
        #Not necessary init as it will be inited with self.curArchive
        self.curArchivedSize = 0
        self.zippedFileInfo = {}

        self.zipStorageState = None


    def saveRegeneratedState(self, encZipFileFullPath, zipFileFullPath):
        ############################
        #Save info for zipped files
        ############################
        s = json.dumps(self.zippedFileInfoRegenerating, sort_keys=True, indent=4)
        f = open(zipFileFullPath.replace('.zip', '.log'),'w')
        f.write(s)
        f.close()
        self.encCopier.copy(zipFileFullPath.replace('.zip', '.log'), encZipFileFullPath.replace('.enc', '.enclog'))
        self.zippedFileInfoRegenerating = {}

        
    def getZipFile(self, encrtypedZipFileFullPath):
        zipFileFullPath = os.path.join(self.decryptionWorkingDir, 
                os.path.basename(encrtypedZipFileFullPath).replace('.enc', '.zip'))
        ########################################
        #TODO: Remove the check and alreays decrypt the file
        ########################################
        if not os.path.exists(zipFileFullPath):
            print 'copy from %s to %s'%(encrtypedZipFileFullPath, zipFileFullPath)
            self.decCopier.copy(encrtypedZipFileFullPath, zipFileFullPath)
        return zipFileFullPath
        
    def readEncryptedZipLog(self, encryptedZipLogPath):
        zipLogPath = os.path.join(self.decryptionWorkingDir, 
                os.path.basename(encryptedZipLogPath).replace('.enclog', '.log'))

        self.decCopier.copy(encryptedZipLogPath, zipLogPath)
        try:
            f = open(zipLogPath,'r')
            res = json.load(f)
            f.close()
            return res
        except IOError:
            return {}

    def updateContentStateForFile(self, encZipFileFullPath):
        encZipLogFilePath = getEncZipLogFilenameFromEncrypted(encZipFileFullPath)
        if not os.path.exists():
            #Regenerate the state info file
            zipFileFullPath = self.getZipFile(encZipFileFullPath)

            #Enumerate all files in the decrypted zip file
            zf = zipClass.ZFile(zipFileFullPath, 'r')
            #Generate a log file if it does not exist
                
            for i in zf.list():
                #yield zipStorageItem(i, zf)
                zf.extract(i, self.workingDir)
                extractedItem = folderStorage.folderStorageItem(self.workingDir, 
                        os.path.join(self.workingDir, i))
                        
                relaPath = transform.formatRelativePath(i)
                self.zippedFileInfoRegenerating[relaPath] = {"zippedTimeStemp": zf.zfile.getinfo(i).date_time, 
                        "headMd5":infoCollector.getHeadContentMd5(extractedItem.getFullPath()), 
                        "parentEncryptedZip":encZipFileFullPath, "size":os.stat(extractedItem.getFullPath()).st_size}

            self.saveRegeneratedState(encZipFileFullPath, zipFileFullPath)
        newLog = readEncryptedZipLog(encZipLogFilePath)
        updateZipLog(newLog)
        
    def checkTimeNotPrecise(self, time1, time2):
        if getTimeInSeconds(time1) > getTimeInSeconds(time2):
            return Ture
        else:
            return False
            
    def updateZipLog(self, newLog):
        for i in newLog:
            relaPath = transform.formatRelativePath(i)
            if self.zipStorageState.has_key(relaPath):
                #Conflict, check if update needed
                if self.checkTimeNotPrecise(newLog[i]["zippedTimeStemp"], self.zipStorageState[relaPath]["zippedTimeStemp"]):
                    print 'update duplicated item:', newLog[i]["zippedTimeStemp"], self.zipStorageState[relaPath]["zippedTimeStemp"]
                    self.zipStorageState[relaPath] = newLog[i]
            else:
                #New item, add it
                self.zipStorageState[relaPath] = newLog[i]
                
    def getItemState(self, relaPath):
        self.readZipStorageState()
        relaPath = transform.formatRelativePath(relaPath)
        return self.zipStorageState[relaPath]
        
    def readZipStorageState(self):
        if self.zipStorageState is None:
            ########################################
            # Update the current storage state, the sync state is different from storage state
            # Storage state is the real time state for all items
            # Do not check the current storage state will have the following problem for zip storage
            # 1. If the source storage has the same file, zip storage will duplicate those files
            #      Those files can be removed by another duplicate finder task
            ########################################
            #print 'zipdir:',self.zipStorageDir
            self.zipStorageState = {}
            for walkingItem in os.walk(self.zipStorageDir):
                print walkingItem
                for j in walkingItem[2]:
                    encZipFileFullPath = transform.transformDirToInternal(os.path.join(walkingItem[0], j))
                    print encZipFileFullPath
                    if encZipFileFullPath.find('.enc') == -1:
                        #Not an encrypted zip file, continue
                        print 'not a encrypted zip file: ',encZipFileFullPath
                        continue
                    self.updateContentStateForFile(encZipFileFullPath)

            
        
    def store(self, item):
        ########################################
        #Check if the target item is already updated
        ########################################
        self.readZipStorageState()
        relaPath = transform.formatRelativePath(item.getRelaPath())

        if getTimeInSeconds(self.zipStorageState[relaPath]["zippedTimeStemp"]) < int(item.getTimestamp()):
            print 'Want to update an older file to a newer file. Ignore it.
            return
        ########################################
        #Check if the target item is already updated?
        ########################################
        if self.curArchive is None:
            self.createNewZip()

        if (self.curArchivedSize > MAX_SINGLE_ARCHIVE_SIZE):
            self.encZip()
            self.createNewZip()
            
        #Add the file to zip
        fullPath = item.getFullPath()
        try:
            existingElem = self.zipContentState[transform.formatRelativePath(i)]
            return
        except:
            pass
        localItem = encZipStorageItem(self.zipStorageDir, self.curArchiveName, relaPath, fullPath)

        ##############################
        #Add the file to zip file
        ##############################
        #print 'copying "%s" to "%s"'%(fullPath, relPath)
        self.curArchive.addfile(unicode(fullPath).encode('gbk'), unicode(relaPath).encode('gbk'))
        self.curArchivedSize += os.stat(fullPath).st_size
        
        self.zippedFileInfo[relaPath] = {"timestamp": os.stat(fullPath).st_mtime, "fullPath":fullPath,
            "headMd5":infoCollector.getHeadContentMd5(fullPath), "parentZip":self.curArchiveName, "size":os.stat(fullPath).st_size,}

        
    ################################################
    # The following methods are only used internally
    ################################################
    def createNewZip(self):
        ####################
        # Create new zip file
        ####################
        self.curArchiveName = transform.transformDirToInternal(
            fileTools.getTimestampWithFreeName(self.workingDir, '.zip'))
        self.curArchive = zipClass.ZFile(self.curArchiveName, 'w')
        self.curArchivedSize = 0
        
    def encZip(self):
        #Must close the zip before encrypt it, otherwise, the file are not integrate
        if self.curArchive is None:
            return
        self.curArchive.close()
        self.curArchive = None
        
        ############################
        # Encrypt the zip file
        ############################
        targetPath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.zipStorageDir, '.enc'))
        print 'copying "%s" to "%s"'%(self.curArchiveName, targetPath)
        #import shutil
        #shutil.copy(self.curArchiveName, targetPath+'.backup.zip')
        self.encCopier.copy(self.curArchiveName, targetPath)
        
        ############################
        # Save info for zipped files
        ############################
        s = json.dumps(self.zippedFileInfo, sort_keys=True, indent=4)
        f = open(self.curArchiveName.replace('.zip', '.log'),'w')
        f.write(s)
        f.close()
        self.encCopier.copy(self.curArchiveName.replace('.zip', '.log'), targetPath.replace('.enc', '.enclog'))
        ############################
        # Update state in storage state
        ############################
        self.updateZipLog(self.zippedFileInfo)
        #Clean the current zipped file info
        self.zippedFileInfo = {}
        
        
        ############################
        # TODO: Remove the zip file and log file?
        ############################
        
            
    def getState(self):
        self.encZip()
        return self.lastState.getState()
