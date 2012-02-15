import inheritableExclusableTagSystem
import libSys
#import libs.ufsDb.ufsDbSys as dbSys
import sessionBase as sessionBase
import objSysV2 as objSys

'''
class objSysInterface:
    def __init__(self, dbSysInst):
        self.dbSysInst = dbSysInst
    def getSameObjs(self, url):
        return [url]
'''
class tagSystemShoveDb(inheritableExclusableTagSystem.tagSystemShoveDb):
    def __init__(self, dbSysInst):
        self.tagSys = inheritableExclusableTagSystem.tagSystemShoveDb.__init__(self, dbSysInst)
        self.objSys = objSys.objSys(dbSysInst)

    def getTags(self, url):
        self.addToObjSysForFullPath(url)
        #print url
        res = inheritableExclusableTagSystem.tagSystemShoveDb.getTags(self, url)
        #print res
        pathTag = []
        for i in self.objSys.getSameObjsForFullPath(url):
            res.extend(inheritableExclusableTagSystem.tagSystemShoveDb.getTags(self, i))
            #print i
            pathTag.append(i)
        res.extend(pathTag)
        res = set(res)
        return list(res)
    def addToObjSysForFullPath(self, fullPath):
        self.objSys.addObjForFullPath(fullPath)
        
    def tag(self, url, tagList):
        self.addToObjSysForFullPath(url)
        return inheritableExclusableTagSystem.tagSystemShoveDb.tag(self, url, tagList)
    def appendTag(self, url, tagList):
        self.addToObjSysForFullPath(url)
        return inheritableExclusableTagSystem.tagSystemShoveDb.appendTag(self, url, tagList)
