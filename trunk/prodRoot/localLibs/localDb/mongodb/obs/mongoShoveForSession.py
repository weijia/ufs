from pymongo import Connection
import UserDict

class nonUnicode: pass

class ShoveForSession(UserDict.DictMixin):
    def __init__(self, dbName, userSession = None, connection = None):
        if connection is None:
            connection = Connection()
        if userSession is None:
            self.user = None
            self.db = connection[dbName].posts
        else:
            self.user = userSession.getUserName()
            self.db = connection[dbName+"_"+self.user].posts
        #self.dbName = dbName

    def __getitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        res = []
        for i in self.db.find({u"key":key}):
            #print i
            res.append(unicode(i[u"value"]))
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
        self.db.remove({"key":key})
        #Insert new
        goodValueList = []
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            goodValueList.append({u"key":key, u"value":i})
        #Set the new value for the specific key
        if 0 == len(goodValueList):
            raise "no Item?"
        self.db.insert(goodValueList)
        
    def getSnapshotTimestamp(self):
        return None
        
    def getSnapshotValueRange(self, key, timestamp, start, cnt):
        if type(key) != unicode:
            raise nonUnicode
        res = []
        if cnt is None:
            f = self.db.find({u"key":key}).skip(start)
        else:
            f = self.db.find({u"key":key}).skip(start).limit(cnt)
        for i in f:
            res.append(unicode(i[u"value"]))
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
            goodValueList.append({u"key":key, u"value":i})
        #Set the new value for the specific key
        if 0 == len(goodValueList):
            raise "no Item?"
        self.db.insert(goodValueList)

    def bulkAdd(self, bulkDict):
        '''
        This function is used in jstreeOnCollectionV2
        '''
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
                encValueList.append({u"key":i, u"value":j})
        if 0 == len(encValueList):
            raise "no Item?"
        last = self.db.insert(encValueList)
        #print last

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
            
    def keysWithUsage(self):
        for i,j in self.dataShove.keysWithUsage():
            yield self.encryptor.de(i),j
            
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
def main():
    s = ShoveLike('sizeInfo')
    print s[u"1"]
     
if __name__ == '__main__':
    main()
