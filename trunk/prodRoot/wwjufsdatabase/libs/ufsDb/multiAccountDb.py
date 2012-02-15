import UserDict
import localLibSys
from localLibs.logSys.logSys import *


class ShoveForSession(UserDict.DictMixin):
    def __init__(self, dbName, primaryUser, secondaryUsers, dbSys):
        self.primaryDb = dbSys(primaryUser).getDb(dbName)
        #cl("creating db for:"+primaryUser.username)
        self.secondaryDbList = [self.primaryDb]
        for i in secondaryUsers:
            self.secondaryDbList.append(dbSys(i).getDb(dbName))
            #cl("creating db for:"+i.username)
    def __getitem__(self, key):
        res = []
        for i in self.secondaryDbList:
            try:
                l = i[key]
                res.extend(l)
            except KeyError:
                pass
        if len(res) == 0:
            raise KeyError
        return list(set(res))

    def __setitem__(self, key, value):
        self.primaryDb.__setitem__(key, value)
        
    def __delitem__(self, key):
        self.primaryDb.__delitem__(key)
        
    def getSnapshotValueRange(self, key, timestampStr, start, cnt):
        res = []
        for i in self.secondaryDbList:
            l = i.getSnapshotValueRange(key, timestampStr, start, cnt)
            res.extend(l)
        return list(set(res))

    def append(self, key, value):
        self.primaryDb.append(key, value)

    def bulkAdd(self, bulkDict):
        self.primaryDb.bulkAdd(bulkDict)
        
    def getSnapshotTimestamp(self):
        return self.primaryDb.getSnapshotTimestamp()
