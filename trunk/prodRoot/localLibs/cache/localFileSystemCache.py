import localLibSys
import uuid
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.objTools as objTools
import shutil

class localFileSystemCache:
    '''
    Will add a record for file system element
    getPath2ObjIdShove: file path -> id
    getObjId2PathShove: id -> file path
    TODO!!!!!!!!!!!!!!!!Move reading id to webapproot, and left only id generation in localDb
    '''
    def __init__(self, dbSys):
        self.dbSys = dbSys
    def getCached(self, objId):
        if objTools.isUuid(objId):
            objId = objTools.getUuid(objId)
        #print 'get cached returns objid:',objId
        return self.dbSys.getObjId2PathShove()[objId][0]
    def getObjId(self, fullPath):
        #format the path
        fullPath = transform.transformDirToInternal(fullPath)
        try:
            #Find the id in database
            id = self.dbSys.getPath2ObjIdShove()[fullPath][0]
            if not objTools.isUuid(id):
                id = objTools.getUrlForUuid(id)
            #print 'existing id:', id
            return id
        except KeyError:
            #Not in db, add a new id for the obj
            newId = unicode(uuid.uuid4())
            #Add ref for 2 database
            self.dbSys.getPath2ObjIdShove()[fullPath] = objTools.getUrlForUuid(newId)
            self.dbSys.getObjId2PathShove()[newId] = fullPath
            return newId
    def moveCached(self, src, dst):
        self.dbSys.getDb("movedItemDb")[dst] = src
        shutil.move(src, dst)
        try:
            #Find the id in database
            id = self.dbSys.getPath2ObjIdShove()[src][0]
            #If no exception, the object is in database, so need to update the new path
            self.dbSys.getObjId2PathShove()[id] = dst
        except KeyError:
            pass

            
            
if __name__=='__main__':
    import localLibs.test.testDbSys as testDbSys
    d = testDbSys.testDbSys()
    l = localFileSystemCache(d)
    i = l.getObjId(u'd:/tmp/')
    print i
    p = l.getCached(i)
    print p
    