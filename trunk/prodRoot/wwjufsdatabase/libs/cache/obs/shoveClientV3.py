import socketimport UserDict
from struct import *
class sharedDb:
    def __init__(self):
        self.data = ''
        self.HOST = '127.0.0.1'    # The remote host
        self.PORT = 8806              # The same port as used by the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
    def get(self, key, dbName):        self.s.send(u'1\n%s\n\n%s\n'%(unicode(key),unicode(dbName)))        uniKey = unicode(key)        uniDbName = unicode(dbName)        keyLen = len(unicode        head = pack("hi",
        self.data += self.s.recv(1024)
        print 'key:%s, data received:%s, dbName:%s'%(key, self.data,dbName)
        if self.data.find('\n') != -1:
            l = self.data.split('\n',2)
            self.data = l[1]
            return l[0]
    def set(self, key, value, dbName):
        self.s.send(u'2\n%s\n%s\n%s\n'%(unicode(key),unicode(value), unicode(dbName)))

    def delete(self, key, dbName):
        self.s.send(u'3\n\n\n%s\n'%(unicode(key),unicode(dbName)))

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
    #s['hello'] = 'good'
    #s['my'] = 'ok'
    print s['G:/app/wwj/hello/06-45166.jpg']
     
if __name__ == '__main__':
    main()
