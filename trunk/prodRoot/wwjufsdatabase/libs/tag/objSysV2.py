import localLibSys
import localLibs.collection.objDbAdv as objDb
import localLibs.objSys.objectDatabaseV3 as objClass
#import localLibs.cache.localFileSystemCache
import libs.utils.transform as transform
import os


class objSys:
    def __init__(self, dbSysInst):
        self.dbSysInst = dbSysInst
        self.objDbInst = objDb.objectDatabase()
    def getSameObjsForFullPath(self, fullPath):
        fullPath = transform.transformDirToInternal(fullPath)
        try:
            objFullPathList = self.objDbInst.getSameObjList(fullPath)
            res = []
            for objFullPath in objFullPathList:
                if os.path.exists(objFullPath):
                    res.append(objFullPath)
            return res
        except IOError:
            return []
        
    def addObjForFullPath(self, fullPath):
        fullPath = transform.transformDirToInternal(fullPath)
        try:
            return self.objDbInst.getFsObjFromFullPath(fullPath)
        except IOError:
            return None
        
        
        
        
'''
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
'''