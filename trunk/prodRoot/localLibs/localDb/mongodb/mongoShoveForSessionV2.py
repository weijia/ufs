from pymongo import Connection
import UserDict

class nonUnicode: pass

import datetime
timeFormat = '%Y-%m-%d:%H-%M-%S'
minTime = datetime.datetime(1900, 1, 1, 0, 0)
maxTime = datetime.datetime(3099, 1, 1, 0, 0)

class ShoveForSession(UserDict.DictMixin):
    def __init__(self, dbName, userSession = None, connection = None):
        self.dbName = dbName
        #self.dbName = unicode(dbName)
        if connection is None:
            connection = Connection()
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
            print 'in mongodb:',i
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
            goodValueList.append({"t":datetime.datetime.utcnow(), "db":self.dbName,"user":self.user,"key":key, "value":i})
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
        timestamp = datetime.strptime(timestampStr, timeFormat)
        res = []
        if cnt is None:
            f = self.db.find({"t": {"$lt": timestamp}, "db":self.dbName,"user":self.user,"key":key}).skip(start)
        else:
            f = self.db.find({"t": {"$lt": timestamp}, "db":self.dbName,"user":self.user,"key":key}).skip(start).limit(cnt)
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
            goodValueList.append({"t":datetime.datetime.utcnow(), "db":self.dbName,"user":self.user,"key":key, "value":i})
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
                encValueList.append({"t":datetime.datetime.utcnow(), "db":self.dbName,"user":self.user,"key":i, "value":j})
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
        
    def keysAfter(self, timestampStr):
        #print 'entering iteritems-------------------------------------db:%s, user:%s'%(self.dbName, self.user)
        #e = self.db.find()
        if not (timestampStr is None):
            timestamp = datetime.datetime.strptime(timestampStr, timeFormat)
        else:
            timestamp = datetime.datetime(1900, 1, 1, 0, 0)
        e = self.db.find({"t": {"$gt": timestamp},"db":self.dbName,"user":self.user})
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
    def getInternalTime(self, timeStr, defaultTime = minTime):
        if not (timeStr is None):
            return datetime.datetime.strptime(timeStr, timeFormat)
        else:
            return defaultTime
    def keysDuring(self, fromTimeStamp, beforeTimeStamp):
        '''
        Include fromTimeStamp but does not include beforeTimeStamp
        '''
        print 'entering keysDuring-------------------------------------db:%s, user:%s'%(self.dbName, self.user)
        #e = self.db.find()
        fromTime = self.getInternalTime(fromTimeStamp)
        beforeTime = self.getInternalTime(beforeTimeStamp, maxTime)
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
    def testFunc(self, key):
        #print 'entering iteritems-------------------------------------db:%s, user:%s'%(self.dbName, self.user)
        #e = self.db.find()
        #e = self.db.find({"db":self.dbName,"user":self.user})
        e = self.db.find({"key":key})
        res = []
        for i in e:
            #print i["key"], i["value"]
            #yield i["key"]
            res.append(i["value"])
            #print i["db"]
            #print 'itering item:', i
        return res
    '''
    '''
    def keysWithUsage(self):
        for i,j in self.db.find({"db":self.dbName,"user":self.user,"key":key}).skip(start):
            yield self.encryptor.de(i),j
    '''
    '''
    def hasValue(self, key, value):
        if type(key) != unicode:
            raise nonUnicode
        encryptedKey = self.encryptor.en(key)
        if type(value) != unicode:
            raise nonUnicode
        encryptedValue = self.encryptor.en(value)
        return self.dataShove.hasValue(encryptedKey, encryptedValue)
    def __delitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        encryptedKey = self.encryptor.en(key)
        del self.dataShove[encryptedKey]
    def keys(self):
        encryptedKeys = self.dataShove.keys()
        res = []
        for i in encryptedKeys:
            res.append(self.encryptor.de(key.decode('utf8')))
            
        return res

    def keys(self):
        yield self.enumeratorOfKey()
        
    def enumeratorOfKey(self):
        if type(key) != unicode:
            raise nonUnicode
        for i in encryptedKeys:
            yield self.encryptor.de(key)
        
    def keys(self):
        for i in self.dataShove.keys():
            yield self.encryptor.de(i)
            
            
    def enumValues(self, key):
        for i in self.dataShove.enumValues(self.encryptor.en(key)):
            yield self.encryptor.de(i)
    def enumValuesWithTime(self, key):
        for i, time in self.dataShove.enumValuesWithTime(self.encryptor.en(key)):
            yield (self.encryptor.de(i), time)
            
    def getAllRecords(self):
        for i in self.dataShove.getAllRecords():
            yield (self.encryptor.de(i[0]),self.encryptor.de(i[1]))
    def append(self, key, value):
        if type(key) != unicode:
            raise nonUnicode
        encryptedKey = self.encryptor.en(key)
        if type(value) == unicode:
            value = [value]
        elif type(value) != list:
            raise nonSupportedValueType
        encValueList = []
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            encValueList.append(self.encryptor.en(i))
        self.dataShove.append(encryptedKey, encValueList)
    '''

def importDb(self, objList):
    connection = Connection()
    db = connection["universalMongoDb"].posts
    self.db.insert(objList)

def getDbList():
    connection = Connection()
    db = connection["universalMongoDb"].posts
    return db.distinct("db")


def getSnapshotTimestamp():
    return unicode(datetime.datetime.utcnow().strftime(timeFormat))

def main():
    print getDbList()
    
     
if __name__ == '__main__':
    main()
