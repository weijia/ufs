import threading
import dbus.service
import dbusServiceBase
import Queue
import gtk

INTERFACE_NAME = 'com.wwjufsdatabase.baseThreadService'
############################################################
# This type of service will cause dead lock and the dbus service will not response if background thread are created!!!!!!!
############################################################

class processorThread(threading.Thread):
    def __init__(self, pendingQ):
        threading.Thread.__init__(self)
        self.pendingQ = pendingQ
    def run(self):
        gtk.gdk.threads_enter()
        cnt = 0
        while True:
            '''
            item = self.pendingQ.get()
            print 'get item', item
            if item:
                self.pendingQ.task_done()
                break
            if True:#try:
                print 'calling subClassProcess'
                self.subClassProcess()
                #except:
                pass
            self.pendingQ.task_done()
            '''
            cnt = cnt + 1
            print cnt
        gtk.gdk.threads_leave()
        print 'returning'
    def subClassProcess(self):
        pass

        
class baseThreadService(dbusServiceBase.dbusServiceBase):
    def __init__(self, sessionBus, objectPath, appConfigDictInst = None):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        self.appConfigDictInst = appConfigDictInst
        self.pendingQ = Queue.Queue()
        self.t = processorThread(self.pendingQ)
        self.t.start()
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='s')
    def test(self):
        print "test called"
        return "OK"