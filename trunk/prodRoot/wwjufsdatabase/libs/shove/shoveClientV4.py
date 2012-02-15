import socketimport UserDict
from struct import *from shoveMultiprocessingClient import sharedDb
        import QueuegQ = Queue.Queue()
s = sharedDb()

gQ.put(s)
        
class Shove(UserDict.DictMixin):
    def __init__(self, dbName):
        self.dbName = dbName
    def __getitem__(self, key):
        q = gQ.get()
        v = q.get(key, self.dbName)
        gQ.put(q)
        if len(v) == 0:
            raise KeyError
        return v
    def __setitem__(self, key, value):
        q = gQ.get()
        q.set(key, value, self.dbName)
        gQ.put(q)

    def __delitem__(self, key):
        q = gQ.get()
        q.rm(key, self.dbName)
        gQ.put(q)
        
    def keys(self):
        pass

def main():
    s = Shove('pathNew')
    s['hello'] = 'good'
    s['my'] = 'ok'
    print s['G:/app/wwj/hello/06-45166.jpg']
     
if __name__ == '__main__':
    main()
