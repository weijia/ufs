import UserDict
import sqlite3
import os
'''
import sqlite3
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("create table kv (key text, value integer);")
# <sqlite3.Cursor object at 0x00C62CE0>
d = {'a':1,'b':2}
c.executemany("insert into kv values (?,?);", d.iteritems())
# <sqlite3.Cursor object at 0x00C62CE0>
c.execute("select * from kv;").fetchall()
# [(u'a', 1), (u'b', 2)]
'''
class nonSupportedValueType: pass
class nonUnicode: pass
import sys

class Shove(UserDict.DictMixin):
    '''
    All key, value and returned values are unicode!!!
    '''
    def __init__(self, dbPath):
        self.db = sqlite3.connect(dbPath)
        self.c = self.db.cursor()
        self.c.execute("create table IF NOT EXISTS kv (key text\
            , value text\
            , createapp VARCHAR(512)\
            , owner VARCHAR(512) DEFAULT 'singleUser'\
            , create_date DATE DEFAULT (DATETIME('NOW'))\
            , removed INTEGER DEFAULT 0\
            , deleted_date DATE DEFAULT (JULIANDAY('2030-01-01'))\
            );")

    def __getitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        t = (key,)
        self.c.execute('SELECT * FROM kv WHERE key=? AND removed = 0', t)
        res = []
        for i in self.c:
            res.append(i[1])
        if 0 == len(res):
            raise KeyError
        return res
        
    def __setitem__(self, key, value):
        appname = sys.argv[0]
        if type(key) != unicode:
            raise nonUnicode
        if type(value) == unicode:
            value = [value]
        elif type(value) != list:
            raise nonSupportedValueType
        t = (key,)
        #Remove existing values for key
        self.c.execute('UPDATE kv SET removed = 1, deleted_date = JULIANDAY("NOW") WHERE key=? AND removed = 0', t)
        #Add new values for key
        for i in value:
            if type(i) != unicode:
                raise nonUnicode
            t = (key, i, appname)
            self.c.execute('INSERT INTO kv(key, value, createapp) VALUES(?, ?, ?)', t)
            #print 'inserting ',t
        self.db.commit()
        
    def __delitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        t = (key,)
        self.c.execute('UPDATE kv SET removed = 1, deleted_date = JULIANDAY("NOW") WHERE key=? AND removed = 0', t)
        self.db.commit()

    def keys(self):
        '''
        During enumeration, no insert would be added. Otherwise, the query will not be correct as no timestamp was used here
        '''
        cc = self.db.cursor()
        cc.execute('SELECT DISTINCT key FROM kv WHERE removed = 0')
        for i in cc:
            yield i[1]
    def keysWithUsage(self):
        '''
        During enumeration, no insert would be added. Otherwise, the query will not be correct as no timestamp was used here
        '''
        cc = self.db.cursor()
        cc.execute('SELECT key, COUNT(*) FROM kv WHERE removed = 0 GROUP BY key ORDER BY COUNT(*) DESC')
        #cc.execute('SELECT key, usage from (SELECT COUNT(*) AS usage,key FROM kv WHERE removed = 0 GROUP BY key) ORDER BY usage ASC')
        for i in cc:
            yield i[0],i[1]
    def bulkAdd(self, bulkDict):
        for i in bulkDict:
            self.internalAppend(i, bulkDict[i])
        self.db.commit()
    def internalAppend(self, key, valueOrList):
        appname = sys.argv[0]
        if type(key) != unicode:
            raise nonUnicode
        if type(valueOrList) == unicode:
            valueOrList = [valueOrList]
        elif type(valueOrList) != list:
            raise nonSupportedValueType
        for i in valueOrList:
            if type(i) != unicode:
                raise nonUnicode
            t = (key, i)
            #Check if the item is already there
            self.c.execute('SELECT value FROM kv WHERE key=? AND value=? AND removed = 0', t)
            flag = False
            for j in self.c:
                flag = True
            if flag:
                continue
            t = (key, i, appname)
            self.c.execute('INSERT INTO kv(key, value, createapp) VALUES(?, ?, ?)', t)
            #print 'inserting ',t
    def append(self, key, valueOrList):
        self.internalAppend(key, valueOrList)
        self.db.commit()
    def remove(self, key, valueOrList):
        if type(key) != unicode:
            raise nonUnicode
        if type(valueOrList) == unicode:
            valueOrList = [valueOrList]
        elif type(valueOrList) != list:
            raise nonSupportedValueType
        for i in valueOrList:
            if type(i) != unicode:
                raise nonUnicode
            t = (key, i)
            #print 'removing:%s,%s'%(key,i)
            self.c.execute('UPDATE kv SET removed = 1, deleted_date = JULIANDAY("NOW") WHERE key=? AND value=?', t)
        self.db.commit()
    def getSnapshotTimestamp(self):
        cc = self.db.cursor()
        cc.execute('SELECT JULIANDAY("NOW")')
        for i in cc:
            #print 'returnning stamp:',i
            return i[0]
    def getSnapshotValueRange(self, key, timestamp, start, cnt):
        cc = self.db.cursor()
        if cnt is None:
            #t = (timestamp,key, timestamp, start)
            t = (key, timestamp, start)
            #cc.execute('SELECT value,deleted_date,removed,? FROM kv WHERE key=? AND deleted_date>? ORDER BY create_date LIMIT -1 OFFSET ?', t)
            cc.execute('SELECT DISTINCT value,deleted_date,removed FROM kv WHERE key=? AND deleted_date>? ORDER BY create_date LIMIT -1 OFFSET ?', t)
        else:
            #t = (timestamp,key, timestamp, cnt, start)
            t = (key, timestamp, cnt, start)
            #cc.execute('SELECT value,deleted_date,removed,? FROM kv WHERE key=? AND deleted_date>? ORDER BY create_date LIMIT ? OFFSET ?', t)
            cc.execute('SELECT DISTINCT value,deleted_date,removed FROM kv WHERE key=? AND deleted_date>? ORDER BY create_date LIMIT ? OFFSET ?', t)
        res = []
        for i in cc:
            #print i
            res.append(i[0])
        #raise "stop here"
        #print len(res)
        return res
    def hasValue(self, key, value):
        if type(key) != unicode:
            raise nonUnicode
        if type(value) != unicode:
            raise nonUnicode
        cc = self.db.cursor()
        t = (key, value)
        cc.execute('SELECT * FROM kv WHERE key=? AND value = ? AND removed = 0', t)
        for i in cc:
            return True
        return False
    def enumValuesWithTime(self, key):
        res = []
        for i in self.__getitem__(key):
            res.append((i, 0))
        return res
        
    def enumValues(self, key):
        '''
        During enumeration, no insert would be added. Otherwise, the query will not be correct as no timestamp was used here
        '''
        t = self.getSnapshotTimestamp()
        maxEnumLen = 100
        start = 0
        while True:
            r = self.getSnapshotValueRange(key, t, start, maxEnumLen)
            start = start+maxEnumLen
            for i in r:
                yield i
            print len(r)
            if len(r) < maxEnumLen:
                break
        