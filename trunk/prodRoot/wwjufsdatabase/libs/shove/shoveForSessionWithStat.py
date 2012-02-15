from pymongo import Connection
import UserDict

class nonUnicode: pass

class ShoveForSession(UserDict.DictMixin):
    def __init__(self, shoveForSessionInst, statDb):
        self.db = shoveForSessionInst
        self.statDb = statDb

    def __getitem__(self, key):
        return self.db[key]

    def __setitem__(self, key, value):
        self.db[key] = value
        #Update after the set is successful
        self.statDb[key] = self.db.getKeyCnt(key)
        
    def getSnapshotTimestamp(self):
        return self.db.getSnapshotTimestamp()
        
    def getSnapshotValueRange(self, key, timestamp, start, cnt):
        return self.db.getSnapshotValueRange(self, key, timestamp, start, cnt)

    def append(self, key, value):
        '''
        #This value will be called in info collection from infoDb
        '''
        self.db.append(key, value)
        #Update after the set is successful
        self.statDb[key] = self.db.getKeyCnt(key)

    def bulkAdd(self, bulkDict):
        '''
        This function is used in jstreeOnCollectionV2
        '''
        self.db.bulkAdd(bulkDict)
        for i in bulkDict:
            #Update after the set is successful
            self.statDb[i] = self.db.getKeyCnt(i)

    
    def keysWithUsage(self):
        for i in self.statDb.keys():
            yield i, self.statDb[i]
    
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
def main():
    s = ShoveLike('sizeInfo')
    print s[u"1"]
     
if __name__ == '__main__':
    main()
