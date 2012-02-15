import asyncore
import socket
from multiprocessing import Process, Queue
import libSys
import libs.localDb.dictShoveDb as dictShoveDb

class EchoHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, q):
        self.q = q
        asyncore.dispatcher_with_send.__init__(self, sock)
        
    def handle_read(self):
        data = self.recv(8192)
        self.send(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port, q):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q = q
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock, q)

            
        
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

            
            
def startServer(dbName):
    s = dictDbServer()
    q = Queue()
    p = Process(target=s.requestProcessor, args=(q,))
    p.start()
    server = EchoServer('localhost', 8080, q)
    asyncore.loop()
            
