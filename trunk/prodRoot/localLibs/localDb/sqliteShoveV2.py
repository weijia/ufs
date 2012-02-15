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

class Shove(UserDict.DictMixin):
    '''
    All key, value and returned values are unicode!!!
    '''
    def __init__(self, dbPath, notUsed = None):
        print dbPath
        if not os.path.exists(dbPath):
            import glob
            pattern = os.path.join(os.path.dirname(dbPath), os.path.basename(dbPath).split('.')[0]+".*")
            print pattern
            dbPath = glob.glob(pattern)
            if len(dbPath) == 1:
                dbPath = dbPath[0]
            else:
                if len(dbPath) > 1:
                    raise "db not exist"
        print dbPath        
        self.db = sqlite3.connect(dbPath)
        self.c = self.db.cursor()
        try:
            #The value may contain \n so only use blob as value type
            self.c.execute("create table kv (key text, value text, timeEnter DATE);")
        except sqlite3.OperationalError:
            #Database exist, it's OK
            pass

    def __getitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        t = (key,)
        self.c.execute('select * from kv where key=?', t)
        res = []
        for i in self.c:
            res.append(i[1])
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
        t = (key,)
        self.c.execute('delete from kv where key=?', t)
        for i in value:
            if type(i) != unicode:
                raise nonUnicode
            t = (key, i)
            try:
                self.c.execute('insert into kv values(? , ?, datetime("now"))', t)
            except sqlite3.OperationalError:
                self.c.execute('insert into kv values(? , ?)', t)
            #print 'inserting ',t
        self.db.commit()
        
    def __delitem__(self, key):
        if type(key) != unicode:
            raise nonUnicode
        t = (key,)
        self.c.execute('delete from kv where key=?', t)
        self.db.commit()
        
    def keys(self):
        cc = self.db.cursor()
        cc.execute('select DISTINCT key from kv')
        for i in cc:
            yield i[0]
    def getAllRecords(self):
        cc = self.db.cursor()
        cc.execute('select * from kv')
        for i in cc:
            yield i
    def enumValues(self, key, startTime = 0):
        cc = self.db.cursor()
        t = (key, )
        #print 'get values for key:',key
        '''
        The ROW ID will be monotonically increasing unique when certain condition are met. Check sqlite document
        '''
        cc.execute('SELECT value, ROWID FROM kv WHERE key=? AND ROWID>? ORDER BY ROWID ASC', t)
        for i in cc:
            yield i[0]
    def enumValuesWithTime(self, key, startTime = 0):
        cc = self.db.cursor()
        t = (key, startTime,)
        #print 'get values for key:',key
        cc.execute('SELECT value, ROWID FROM kv WHERE key=? AND ROWID>? ORDER BY ROWID ASC', t)
        for i in cc:
            yield (i[0], i[1])
