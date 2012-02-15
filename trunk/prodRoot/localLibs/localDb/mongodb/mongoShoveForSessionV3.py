from pymongo import Connection
from pymongo import errors
import UserDict

class nonUnicode: pass
'''
import datetime
timeFormat = '%Y-%m-%d:%H-%M-%S'
minTime = datetime.datetime(1900, 1, 1, 0, 0)
maxTime = datetime.datetime(3099, 1, 1, 0, 0)
'''
import time

def getSnapshotTimestamp():
    return unicode(str(time.time()))

class ShoveForSession(UserDict.DictMixin):
    def __init__(self, dbName, userSession = None, connection = None):
        self.dbName = dbName
        #self.dbName = unicode(dbName)
        if connection is None:
            cnt = 0
            while True:
                try:
                    connection = Connection()
                    break
                except errors.AutoReconnect:
                    cnt += 1
                    if cnt > 10:
                        raise "retried too many times"
                    pass
                time.sleep(5)
        if userSession is None:
            self.user = None
        else:
            self.user = unicode(userSession.getUserName())
        self.db = connection["universalMongoDb"].posts
        #self.dbName = dbName

    def __getitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        res = []
        #print 'in mongo, requesting key:%s, dbName:%s, user:%s'%(key, self.dbName, self.user)
        for i in self.db.find({"db":self.dbName,"user":self.user,"key":key}):
            #print 'in mongodb:',i
            res.append(unicode(i["value"]))
        if 0 == len(res):
            raise KeyError
        return res

    def __setitem__(self, key, value):
        if type(key) != unicode:
            raise nonUnicode
        if type(value) == unicode:
            value = [value]
        elif type(value) != list:
            raise nonSupportedValueType
        #Remove existing
        self.db.remove({"db":self.dbName,"user":self.user,"key":key})
        #Insert new
        goodValueList = []
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            goodValueList.append({"ta":time.time(), "db":self.dbName,"user":self.user,"key":key, "value":i})
        #Set the new value for the specific key
        if 0 == len(goodValueList):
            raise "no Item?"
        self.db.insert(goodValueList)
    def __delitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        self.db.remove({"db":self.dbName,"user":self.user,"key":key})
        
    def getSnapshotValueRange(self, key, timestampStr, start, cnt):
        if type(key) != unicode:
            raise nonUnicode
        timestamp = float(timestampStr)
        res = []
        if cnt is None:
            f = self.db.find({"ta": {"$lt": timestamp}, "db":self.dbName,"user":self.user,"key":key}).skip(start)
        else:
            f = self.db.find({"ta": {"$lt": timestamp}, "db":self.dbName,"user":self.user,"key":key}).skip(start).limit(cnt)
        for i in f:
            res.append(unicode(i["value"]))
        return res

    def append(self, key, value):
        '''
        #This value will be called in info collection from infoDb
        '''
        if type(key) != unicode:
            raise nonUnicode
        if type(value) == unicode:
            value = [value]
        elif type(value) != list:
            raise nonSupportedValueType
        #Insert new
        goodValueList = []
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            #Check if the value is already in database
            if self.db.find({"db":self.dbName,"user":self.user,"key":key, "value":i}).count()>0:
                #Item exist, skip
                continue
            goodValueList.append({"ta":time.time(), "db":self.dbName,"user":self.user,"key":key, "value":i})
        #Set the new value for the specific key
        if 0 == len(goodValueList):
            #raise "no Item?"
            return
        self.db.insert(goodValueList)

    def bulkAdd(self, bulkDict):
        '''
        This function is used in jstreeOnCollectionV2
        '''
        if 0 == len(bulkDict):
            return
        for i in bulkDict:
            value = bulkDict[i]
            if type(i) != unicode:
                raise nonUnicode
            if type(value) == unicode:
                value = [value]
            elif type(bulkDict[i]) != list:
                raise nonSupportedValueType
            encValueList = []
            for j in value:
                if type(j) != unicode:
                    raise nonUnicodeValue
                encValueList.append({"ta":time.time(), "db":self.dbName,"user":self.user,"key":i, "value":j})
        if 0 == len(encValueList):
            raise "no Item?"
        last = self.db.insert(encValueList)
        #print last
    def getKeyCnt(self, key):
        return self.db.find({"db":self.dbName,"user":self.user,"key":key}).count()
        
    def keys(self):
        #print 'entering iteritems-------------------------------------db:%s, user:%s'%(self.dbName, self.user)
        #e = self.db.find()
        e = self.db.find({"db":self.dbName,"user":self.user})
        #e = self.db.find()
        res = []
        for i in e:
            #print i["key"], i["value"]
            #print i["db"], i["user"]
            
            #if not ((i["db"] == self.dbName) and (i["user"] == self.user)):
            #    print '------------------------------------------got unwanted value',i["db"], i["user"]
            #    continue
            yield i["key"]
            #res.append(i["key"])
            #print 'itering item:', i
        #return res
    '''
    def keysAfter(self, timestampStr):
        #print 'entering iteritems-------------------------------------db:%s, user:%s'%(self.dbName, self.user)
        #e = self.db.find()
        if not (timestampStr is None):
            timestamp = datetime.datetime.strptime(timestampStr, timeFormat)
        else:
            timestamp = datetime.datetime(1900, 1, 1, 0, 0)
        e = self.db.find({"ta": {"$gt": timestamp},"db":self.dbName,"user":self.user})
        #e = self.db.find()
        res = []
        for i in e:
            #print i["key"], i["value"]
            #print i["db"], i["user"]
            
            #if not ((i["db"] == self.dbName) and (i["user"] == self.user)):
            #    print '------------------------------------------got unwanted value',i["db"], i["user"]
            #    continue
            yield i["key"]
            #res.append(i["key"])
            #print 'itering item:', i
        #return res
    '''
    '''
    def keysDuring(self, fromTimeStamp, beforeTimeStamp):
        print 'entering keysDuring-------------------------------------db:%s, user:%s'%(self.dbName, self.user)
        #e = self.db.find()
        fromTime = getInternalTime(fromTimeStamp)
        beforeTime = getInternalTime(beforeTimeStamp, maxTime)
        print fromTime, beforeTime
        #e = self.db.find({"or":[{"t": {"$gte": fromTime}, "t": {"$lt": beforeTime}},{"t":{"$exists":"false"}}],
        #    "db":self.dbName,"user":self.user}).distinct("key")
        e = self.db.find({"t":{"$exists":False}, "db":self.dbName,"user":self.user}).distinct("key")
        #e = self.db.find({"t": {"$gte": fromTime}, "db":self.dbName,"user":self.user}).distinct("key")
        #e = self.db.find()
        res = []
        for i in e:
            #print i["key"], i["value"]
            #print i["db"], i["user"]
            #print i
            yield i
            #if not ((i["db"] == self.dbName) and (i["user"] == self.user)):
            #    print '------------------------------------------got unwanted value',i["db"], i["user"]
            #    continue
            #yield i["key"]
            #res.append(i["key"])
            #print 'itering item:', i
        #return res        
    '''
    def getSnapshotTimestamp(self):
        return getSnapshotTimestamp()

def importDb(objList):
    connection = Connection()
    db = connection["universalMongoDb"].posts
    db.insert(objList)

def getDbList():
    connection = Connection()
    db = connection["universalMongoDb"].posts
    return db.distinct("db")
'''
def getUniversalTime(t):
    return unicode(t.strftime(timeFormat))
def getInternalTime(timeStr, defaultTime = minTime):
    if not (timeStr is None):
        return datetime.datetime.strptime(timeStr, timeFormat)
    else:
        return defaultTime
'''
def exportDb(fromTimeStampStr = None, beforeTimeStampStr = None, exporter = 'home-ibm'):
    '''
    Include fromTimeStamp but does not include beforeTimeStamp
    '''
    connection = Connection()
    db = connection["universalMongoDb"].posts
    fromTimeStamp = float(fromTimeStampStr)
    beforeTimeStamp = float(beforeTimeStampStr)
    print fromTimeStamp, beforeTimeStamp
    e = db.find({"ta": {"$gte": fromTimeStamp, "$lt": beforeTimeStamp}})
    dupFinder = {}
    res = []
    for i in e:
        #print i
        
        #item validation, check if "key", "value" exists
        if (not i.has_key("key")) or (not i.has_key("value")):
            print 'no key or value:', i
            continue
        if i.has_key("ta"):
            ta = i["ta"]
        else:
            ta = time.time()
        #Check if there is duplicated item
        if dupFinder.has_key(i["key"]+i["value"]+str(i["db"])+str(i["user"])):
            #Check if duplicated item has found
            existing = dupFinder[i["key"]+i["value"]+str(i["db"])+str(i["user"])]
            if (i["key"] == existing["key"]) and (i["value"] == existing["value"]) and (i["db"] == existing["db"]) and (i["user"] == existing["user"]):
                print 'duplicated item: ', i
            continue
        else:
            dupFinder[i["key"]+i["value"]+str(i["db"])+str(i["user"])] = i
        item = {"ta": ta, "key": i["key"], "value": i["value"], "db":i["db"], "user":i["user"], "exporter": exporter, "valid": True}
        res.append(item)
    return res

def main():
    print getDbList()
    
     
if __name__ == '__main__':
    main()
