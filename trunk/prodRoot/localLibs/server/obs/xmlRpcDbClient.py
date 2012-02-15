import UserDict
import xmlrpclib
import libSys
class nonUnicode: pass
import libs.utils.encodingTools as encodingTools

class ShoveForSession(UserDict.DictMixin):
    def __init__(self, dbName, userSession = None):
        self.proxy = xmlrpclib.ServerProxy("http://localhost:8806/", allow_none=1)
        self.dbName = dbName
        if userSession is None:
            self.user = None
        else:
            self.user = userSession.getUserName()

    def __getitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        res = self.proxy.getValues(self.user, self.dbName, key)
        if res is None:
            raise KeyError
        if type(res) != list:
            raise 'non list'
        #print res
        uniRes = []
        for i in res:
            uniRes.append(encodingTools.decodeToUnicode(i))
        return uniRes

    def __setitem__(self, key, value):
        if type(key) != unicode:
            raise nonUnicode
        if type(value) == unicode:
            value = [value]
        elif type(value) != list:
            raise nonSupportedValueType
        goodValueList = []
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            goodValueList.append(i)
        #Set the new value for the specific key
        self.proxy.setValues(self.user, self.dbName, key, goodValueList)
    def getSnapshotTimestamp(self):
        return self.proxy.getSnapshotTimestamp(self.user, self.dbName)
        
    def getSnapshotValueRange(self, key, timestamp, start, cnt):
        res = self.proxy.getSnapshotValueRange(self.user, self.dbName, key, timestamp, start, cnt)
        uniRes = []
        #print '++++++++++++++++++++++++++++++++++++++++++++'
        #print res
        for i in res:
            uniRes.append(encodingTools.decodeToUnicode(i))
        return uniRes

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
        uniValueList = []
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            uniValueList.append(i)
        #print 'adding:',uniValueList
        self.proxy.appendValues(self.user, self.dbName, key, uniValueList)

    def bulkAdd(self, bulkDict):
        '''
        This function is used in jstreeOnCollectionV2
        '''
        encDict = {}
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
                encValueList.append(j)
            encDict[i] = encValueList
        last = self.proxy.bulkAdd(self.user, self.dbName, encDict)
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
