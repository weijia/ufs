import libSys


class noneEncryptor:
    def __init__(self, encKey = None):
        self.encKey = encKey
    def de(self, encryptedStr):
        return encryptedStr
    def en(self, encryptingStr):
        return encryptingStr
import libs.utils.xorEncryptorUnicode as xorEncryptorUnicode


class nonUnicodeError:
    pass

class simpleEncryptor:
    def __init__(self, encKey):
        self.encKey = encKey
        
    def de(self, encryptedStr):
        if type(encryptedStr) == unicode:
            return xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptedStr)
        raise nonUnicodeError
        
    def en(self, encryptingStr):
        if type(encryptingStr) == unicode:
            return xorEncryptorUnicode.PEcrypt(self.encKey).Crypt(encryptingStr)
        raise nonUnicodeError

from binHex import binHex
        
class encryptorTxtOut:
    def __init__(self, encKey, encryptor = simpleEncryptor):
        '''
        All strings should be unicode
        '''
        self.binHex = binHex()
        self.encryptor = encryptor(encKey)
        
    def de(self, encryptedStr):
        if type(encryptedStr) == unicode:
            try:
                return self.encryptor.de(self.binHex.de(encryptedStr))
            except ValueError:
                print 'unknown error, str:', encryptedStr
                raise ValueError
        raise nonUnicodeError
        
    def en(self, encryptingStr):
        if type(encryptingStr) == unicode:
            return self.binHex.en(self.encryptor.en(encryptingStr))
        raise nonUnicodeError


import UserDict

class nonSupportedValueType: pass
class nonUnicode: pass
class nonUnicodeValue: pass



class ShoveLike(UserDict.DictMixin):
    '''
    Both key and value should be unicode
    '''
    def __init__(self, shoveObj, notUsed = None, encryptor = encryptorTxtOut, simpleKey = 'simpleKey'):
        self.dataShove = shoveObj
        self.encryptor = encryptor(simpleKey)
    def __getitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        #print 'requesting key:', key
        encryptedKey = self.encryptor.en(key)
        #print 'target key:',encryptedKey
        #The following always return an array
        encryptedValueList = self.dataShove[encryptedKey]
        res = []
        for i in encryptedValueList:
            res.append(self.encryptor.de(i))
        return res

    def __setitem__(self, key, value):
        if type(key) != unicode:
            raise nonUnicode
        encryptedKey = self.encryptor.en(key)
        if type(value) == unicode:
            value = [value]
        elif type(value) != list:
            raise nonSupportedValueType
        encryptedValueList = []
        #Encrypt all values
        for i in value:
            if type(i) != unicode:
                raise nonUnicodeValue
            v = self.encryptor.en(i)
            encryptedValueList.append(v)
            #print 'appending:', self.encryptor.de(v)
        #Set the new value for the specific key
        self.dataShove[encryptedKey] = encryptedValueList
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
    '''
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
    '''
        
    def keys(self):
        #print 'in encrypted list shove like'
        for i in self.dataShove.keys():
            #print i
            try:
                yield self.encryptor.de(i)
            except ValueError:
                continue
    def keysAfter(self, timestamp):
        #print 'in encrypted list shove like'
        for i in self.dataShove.keysAfter(timestamp):
            #print i
            try:
                yield self.encryptor.de(i)
            except ValueError:
                continue
    def keysDuring(self, fromTimeStamp, beforeTimeStamp):
        #print 'in encrypted list shove like'
        for i in self.dataShove.keysDuring(fromTimeStamp, beforeTimeStamp):
            #print i
            try:
                yield self.encryptor.de(i)
            except ValueError:
                continue
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
    def getSnapshotTimestamp(self):
        return self.dataShove.getSnapshotTimestamp()
    def getSnapshotValueRange(self, key, timestamp, start, cnt):
        resRange = self.dataShove.getSnapshotValueRange(self.encryptor.en(key), timestamp, start, cnt)
        res = []
        for i in resRange:
            res.append(self.encryptor.de(i))
        return res
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
    def bulkAdd(self, bulkDict):
        encDict = {}
        for i in bulkDict:
            value = bulkDict[i]
            if type(i) != unicode:
                raise nonUnicode
            encryptedKey = self.encryptor.en(i)
            if type(value) == unicode:
                value = [value]
            elif type(bulkDict[i]) != list:
                raise nonSupportedValueType
            encValueList = []
            for j in value:
                if type(j) != unicode:
                    raise nonUnicodeValue
                encValueList.append(self.encryptor.en(j))
            encDict[self.encryptor.en(i)] = encValueList
        self.dataShove.bulkAdd(encDict)
    '''
    def testFunc(self, key):
        if type(key) != unicode:
            raise nonUnicode
        #print 'requesting key:', key
        encryptedKey = self.encryptor.en(key)
        #print 'target key:',encryptedKey
        #The following always return an array
        encryptedValueList = self.dataShove.testFunc(encryptedKey)
        res = []
        print key.encode('gbk', 'replace')
        for i in encryptedValueList:
            v = self.encryptor.de(i)
            res.append(v)
            print v.encode('gbk', 'replace')
        return res
    '''