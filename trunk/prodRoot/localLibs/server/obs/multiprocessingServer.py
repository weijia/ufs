from multiprocessing.managers import BaseManager,Process
import Queue

class QueueManager(BaseManager): pass


class multiprocessingServer:
    def startServer(self):
        self.reqQ = Queue.Queue()
        QueueManager.register('getReqQ', callable=lambda:self.reqQ)
        self.resQ = Queue.Queue()
        QueueManager.register('getResQ', callable=lambda:self.resQ)
        m = QueueManager(address=('', 8809), authkey='abracadabra')
        s = m.get_server()
        #p = Process(target=processor, args=(self.reqQ,))
        #p.start()
        s.serve_forever()
        


if __name__ == '__main__':
    s = multiprocessingServer()
    s.startServer()