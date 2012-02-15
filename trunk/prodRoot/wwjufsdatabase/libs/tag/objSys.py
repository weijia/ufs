class objSysInterface:
    def __init__(self, dbSysInst):
        self.dbSysInst = dbSysInst
    def getSameObjs(self, url):
        return [url]

import localLibSys
#TODO!!!!!!!!!!!!!!!!Move reading id to webapproot, and left only id generation in localDb
import libSys
import localLibs.localTasks.infoCollector as dbSizeMod
#import localLibs.cache.localFileSystemCache
import os
import libs.utils.transform as transform


def isBaseNameIdentical(origFullPath, targetFullPath):
    if os.path.basename(targetFullPath) == os.path.basename(origFullPath):
        return True
    else:
        return False

def isIdentical(origHeadMd5, origFullPath, targetHeadMd5, targetFullPath):
    if (origHeadMd5 is None) or (targetHeadMd5 is None):
        #MD5 is None, only check basename
        return isBaseNameIdentical(origFullPath, targetFullPath)
    else:
        return origHeadMd5 == targetHeadMd5



class objSys:
    def __init__(self, dbSysInst):
        self.dbSysInst = dbSysInst
    def getSameObjsForFullPath(self, fullPath):
        fullPath = transform.transformDirToInternal(fullPath)
        #0. Return empty for dir
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #To do to catch exception of file not exist
        if os.path.isdir(fullPath):
            return []
        #1. First find the items marked as the same
        
        #2. Check same content files
        #2.1 Check same size
        sizeDbInst = dbSizeMod.InfoDb(self.dbSysInst)
        size = sizeDbInst.getInfo(dbSizeMod.localPathElement(fullPath, self.dbSysInst))
        #print 'got info from db:',fullPath, size
        itemPathList = sizeDbInst.getItemWithInfo(size)
        #2.2 Check content of same size
        #print 'with the same size:',itemPathList
        if 0 != len(itemPathList):
            #print 'check data for the items'
            #2.2.1 Size same, compare content if possible, other wise check if the name is the same
            res = []
            headDb = dbSizeMod.InfoDb(self.dbSysInst, dbSizeMod.getHeadContentMd5, "headInfo")
            #Replace try after got the actual exception raised by path does not exist
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            try:#if True:
                origMd5 = headDb.getInfo(dbSizeMod.localPathElement(fullPath, self.dbSysInst))
            except IOError:#else:
                origMd5 = None
            for i in itemPathList:
                if i == fullPath:
                    continue
                if origMd5 is None:
                    targetMd5 = None
                else:
                    #Replace try after got the actual exception raised by path does not exist
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    try:#if True:
                        targetMd5 = headDb.getInfo(dbSizeMod.localPathElement(i, self.dbSysInst))
                    except IOError:#else:
                        targetMd5 = None
                if isIdentical(origMd5, fullPath, targetMd5, i):
                    res.append(i)
            return res
        return []
    def addObjForFullPath(self, fullPath):
        #headDb = dbSizeMod.InfoDb(self.dbSysInst, dbSizeMod.getHeadContentMd5, "headInfo")
        sizeDbInst = dbSizeMod.InfoDb(self.dbSysInst)
        #headDb.getInfo(dbSizeMod.localPathElement(fullPath, self.dbSysInst))
        sizeDbInst.getInfo(dbSizeMod.localPathElement(fullPath, self.dbSysInst))
        
        
        
        
def main():
    import libs.ufsDb.ufsDbSys as dbSys
    o = objSys(dbSys.dbSysSmart())
    print o.getSameObjsForFullPath("D:/Profiles/q19420/My Documents/Bluetooth/Inbox/CAM_0001.jpg")
    print '-----------------------------------------------------------'
    print o.getSameObjsForFullPath('D:\\proj\\LTE\\CAM_0001.jpg')
    print o.getSameObjsForFullPath('D:/proj/LTE/LTE-BCU2-procedure.xls')
    print '-----------------------------------------------------------'
    print o.getSameObjsForFullPath('D:\\proj\\LTE\\bcu2-physap.xls')
    
    
if __name__=='__main__':
    main()