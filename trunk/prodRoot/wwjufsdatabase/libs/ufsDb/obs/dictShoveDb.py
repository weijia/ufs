import libSys
import os
import libs.utils.misc as misc

gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

misc.ensureDir(gAppPath)
misc.ensureDir(gDbPath)

#------------------------------------------------------------------
#Local database
try:
    import libs.GAE.ufsDbGaeListShove as listShove
    import libs.GAE.ufsDbGaeShove as shove
except ImportError:
    import sys
    import os
    c = os.getcwd()
    while c.find('prodRoot') != -1:
      c = os.path.dirname(c)
    #print c
    sys.path.insert(0, os.path.join(c,'prodRoot'))
    import localLibs.localDb.sqliteShoveV2 as shove
    import libs.shove.encryptedListShove as encryptedListShove
    import libs.shove.encryptedShoveV4 as encryptedShove


def getListDbLocal(dbName):
    s = shove.Shove(os.path.join(gDbPath,'%s.sqliteDict'%dbName)+'.enc')
    return encryptedListShove.ShoveLike(s)

def getDbLocal(dbName):
    s = shove.Shove(os.path.join(gDbPath,'%s.sqliteDict'%dbName)+'.enc')
    return encryptedShove.ShoveLike(s)

#------------------------------------------------------------------
#Interface used for system
def getListDbForDirCacheDb(dbName):
    return getListDbLocal(dbName)
    
def getDbForDirCacheDb(dbName):
    return getDbLocal(dbName)
    
def getDbForTag(dbName):
    return getListDbLocal(dbName)
    
    
if __name__ == '__main__':
    existing = []
    '''
    for i in os.listdir(gDbPath):
        existing.append(i.split('.')[0])
        print i
    for i in existing:
        newDb = getListDbLocal(i+'.withTime')
        oldDb = getListDbLocal(i)
        for j in oldDb.keys():
            print j
            newDb[j] = oldDb[j]
            
    '''
    for i in os.listdir(gDbPath):
        existing.append(i.split('.')[0])
        print i
        break
    for i in existing:
        newDb = getListDbLocal(i+'.withTime')
        for j in newDb.dataShove.getAllRecords():
            print j

