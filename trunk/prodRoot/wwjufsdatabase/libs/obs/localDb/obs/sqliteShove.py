import UserDict
import sqlite3

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


class Shove(UserDict.DictMixin):
    def __init__(self, dbPath, cacheDbPath):
        self.db = sqlite3.connect(dbPath)
        self.c = self.db.cursor()
        try:
            #The value may contain \n so only use blob as value type
            self.c.execute("create table kv (key text, value text);")
        except sqlite3.OperationalError:
            #Database exist, it's OK
            pass

    def __getitem__(self, key):
        t = (key,)
        self.c.execute('select * from kv where key=?', t)
        for i in self.c:
            return i[1]
        raise KeyError
        
    def __setitem__(self, key, value):
        t = (key, value)
        self.c.execute('insert into kv values(? , ?)', t)
        self.db.commit()
        
    def __delitem__(self, key):
        t = (key,)
        self.c.execute('delete from kv where key=?', t)
        self.db.commit()
        
    def keys(self):
        pass

def main():
    s = Shove('pathNew')
    s['hello'] = 'good'
    s['my'] = 'ok'
    print s['hello']
    #print s['G:/app/wwj/hello/06-45166.jpg']
     
if __name__ == '__main__':
    main()
