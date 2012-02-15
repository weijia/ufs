import os
import localLibSys

import wwjufsdatabase.libs.utils.transform as transform
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
import wwjufsdatabase.libs.utils.fileTools as fileTools
import wwjufsdatabase.libs.utils.misc as misc
import desktopApp.lib.compress.zipClass as zipClass
import folderStorageV3 as folderStorage
import localLibs.localTasks.infoCollector as infoCollector
import wwjufsdatabase.libs.utils.simplejson as json


MAX_SINGLE_ARCHIVE_SIZE = 5*1024*1024

def getTimeTuple(seconds):
    t = time.localtime(seconds)
    return (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

def getEncZipLogFilenameFromEncrypted(encryptedFilePath):
    return encryptedFilePath.replace('.enc', '.enclog')
    
class zipStorageLocalState(folderStorage.folderStorageState):
    def __init__(self, stateDict):
        self.rootStateDict = stateDict
        ###################################
        #Does the child dict change take effect in the parent dict?????
        try:
            self.stateDict = self.rootStateDict["itemStates"]
        except:
            self.rootStateDict["itemStates"] = {}
            self.stateDict = self.rootStateDict["itemStates"]
        try:
            self.zipFileStateDict = self.rootStateDict["zipFileStates"]
        except:
            self.rootStateDict["zipFileStates"] = {}
            self.zipFileStateDict = self.rootStateDict["zipFileStates"]
            
    def isZipFileUpdated(self, item):
        #print 'checking item for update: %s'%item.getItemId(), self.stateDict[item.getItemId()]
        try:
            #Item was recorded, check if timestamp changed
            if self.zipFileStateDict[item.getItemId()]["timestamp"] == item.getTimestamp():
                '''
                #File changed, check hash?
                if self.stateDict[item.getItemId()]["headMd5"] != infoCollector.getHeadContentMd5(item.getFullPath()):
                    return False
                '''
                return False
        except KeyError:
            pass
        return True
    def zipFileUpdate(self, item):
        self.zipFileStateDict[item.getItemId()] = item.getItemInfo()
        
    # def updated(self, item):
        # #print 'checking item for update: %s'%item.getItemId(), self.stateDict[item.getItemId()]
        # try:
            # #Item was recorded, check if timestamp changed
            # if self.stateDict[item.getItemId()]["timestamp"] == item.getTimestamp():
                # '''
                # #File changed, check hash?
                # if self.stateDict[item.getItemId()]["headMd5"] != infoCollector.getHeadContentMd5(item.getFullPath()):
                    # return False
                # '''
                # return False
        # except KeyError:
            # pass
        # return True
            
    def update(self, item):
        self.stateDict[item.getItemId()] = item.getItemInfo()
    def getState(self):
        return self.rootStateDict
        
    def getItemState(self, item):
        return self.stateDict[item.getItemId()]

'''
{
    "15990197630-SysCfg.xml": {
        "headMd5": "2f13161d7594011b47f99a6878475efe", 
        "parentEncZip": "D:/oldmachine/sys/my-sync/pidgin/data/1311527042.02.enc", 
        "size": 15336, 
        "timestamp": 12345678.1
    }, 
'''
# def getTimeInSeconds(timeStructure):
    # finalRes = []
    # for i in timeStructure:
        # finalRes.append(i)
    # finalRes.extend([0,0,0])
    # return time.mktime(finalRes)

class encZipWriteOnlyStorage(folderStorage.storageInterface):
    def __init__(self, lastState, workingDir, zipStorageDir, passwd):
        self.lastState = zipStorageLocalState(lastState)
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
        #The current zipfile object
        self.curArchive = None
        #Not necessary init as it will be inited with self.curArchive
        #The current archived size
        self.curArchivedSize = 0
        
        #The info of files in the current zip file
        self.zippedFileInfo = {}
        
        #The info of the whole storage
        self.zipStorageState = None


    def readEncryptedZipLog(self, encryptedZipLogPath):
        #print encryptedZipLogPath
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
        newLog = self.readEncryptedZipLog(encZipLogFilePath)
        '''
        try:
            self.updateZipLog(newLog)
        except KeyError:
            print 'update content state failed:', encZipLogFilePath, newLog
        '''
        self.updateZipLog(newLog)
            
    def updateZipLog(self, newLog):
        for i in newLog:
            relaPath = transform.formatRelativePath(i)
            if self.zipStorageState.has_key(relaPath):
                #Conflict, check if update needed
                if newLog[i]["timestamp"] > self.zipStorageState[relaPath]["timestamp"]:
                    print 'update duplicated item:', newLog[i]["timestamp"], self.zipStorageState[relaPath]["timestamp"]
                    self.zipStorageState[relaPath] = newLog[i]
            else:
                #New item, add it
                t = newLog[i]["timestamp"]
                self.zipStorageState[relaPath] = newLog[i]
                
    def getItemState(self, relaPath):
        self.readZipStorageState()
        relaPath = transform.formatRelativePath(relaPath)
        return self.zipStorageState[relaPath]
        
    def readZipStorageState(self):
        if self.zipStorageState is None:
            print 'Loading storage state....'
            #print 'zipdir:',self.zipStorageDir
            self.zipStorageState = {}
            for walkingItem in os.walk(self.zipStorageDir):
                #print walkingItem
                for j in walkingItem[2]:
                    encZipFileFullPath = transform.transformDirToInternal(os.path.join(walkingItem[0], j))
                    #print encZipFileFullPath
                    import re
                    if re.search('\.enc$', encZipFileFullPath) is None:
                        #Not an encrypted zip file, continue
                        #print 'not a encrypted zip file: ',encZipFileFullPath
                        continue
                    self.updateContentStateForFile(encZipFileFullPath)
            print 'Storage state loaded'
        
    def store(self, item):
        ########################################
        #Check if the target item is already updated
        ########################################
        self.readZipStorageState()
        relaPath = transform.formatRelativePath(item.getRelaPath())
        
        
        ########################################
        #Check if the target item is already updated
        ########################################
        if self.zipStorageState.has_key(relaPath) and (self.zipStorageState[relaPath]["timestamp"] > 
                        item.getTimestamp()):
            print 'Want to update an older file to a newer file. Ignore it.'
            return

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

        ##############################
        #Add the file to zip file
        ##############################
        #print 'copying "%s" to "%s"'%(fullPath, relPath)
        self.curArchive.addfile(unicode(fullPath).encode('gbk'), unicode(relaPath).encode('gbk'))
        self.curArchivedSize += os.stat(fullPath).st_size
        itemInfo = item.getItemInfo()
        itemInfo["parentEncZip"] = self.curArchiveName.replace(".zip", ".enc")
        self.zippedFileInfo[relaPath] = itemInfo

        
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
        zipFileFolderStorageItem = folderStorage.folderStorageItem(self.zipStorageDir, targetPath)
        self.lastState.zipFileUpdate(zipFileFolderStorageItem)
        
        ############################
        # TODO: Remove the zip file and log file?
        ############################
        
            
    def getState(self):
        self.encZip()
        return self.lastState.getState()
