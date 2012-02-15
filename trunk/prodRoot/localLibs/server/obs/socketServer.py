import asyncore
import socket
import re
import libSys
import libs.localDb.dictShoveDb as dictShoveDb
'''
from multiprocessing import Process, Queue
'''
def rmHeading(s, prefix = '\n'):
    while s[0] == prefix:
        s = s[1:]
    return s
gData = ''
gDbDict = {}
#gDatabase = dictShoveDb.getDb('testingDbServer')

class EchoHandler(asyncore.dispatcher_with_send):
    '''
    def handle_close(self):
        for i in gDbDict.keys():
            gDbDict[i].close()
            del gDbDict[i]
    '''
    def handle_read(self):
        global gData
        gData += self.recv(8192)
        l = gData.split('\n')
        while len(l) > 4:
            #Have a total request, process it
            reqType = unicode(l[0])
            key = unicode(l[1])
            value = unicode(l[2])
            dbName = unicode(l[3])
            print 'get req for %s'%dbName
            try:
                db = gDbDict[dbName]
            except KeyError:
                db = dictShoveDb.getDbV4(dbName)
                gDbDict[dbName] = db
            self.processRequest(reqType, key, value, db)
            l = l[4:]
        gData = '\n'.join(l)
        
    def processRequest(self, reqType, key, value, db):
        if '0' == reqType:
            #End req
            return
        if '1' == reqType:
            #Query
            try:
                self.send(db[key]+'\n')
                print 'find %s = %s'%(key, db[key])
            except KeyError:
                print '%s not exist'%key
                self.send('\n')
        if '2' == reqType:
            print 'set:%s = %s'%(key, value)
            db[key] = value

        

class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

            
'''
class dictDbServer:
    def __init__(self, dbName):
        self.db = dictShoveDb.getDb(dbName)
    def requestProcessor(q):
        reqType, key, value = q.get()
        if 0 == reqType:
            #End req
            return
        if 1 == reqType:
            #Query
            return self.db[key]
        if 2 == reqType:
            self.db[key] = value
'''
            
            
def startServer():
    #s = dictDbServer()
    server = EchoServer('localhost', 8806)
    asyncore.loop()
            

def main():
    startServer()
     
if __name__ == '__main__':
    main()
