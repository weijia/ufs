import dbusServiceBase
import threading
import dbus.service
import Queue
import localLibs.localTasks.advCollectionProcessorV2 as advCollectionProcessor
import wwjufsdatabase.libs.utils.transform as transform
import gtk
############################################################
# This type of service will cause dead lock and the dbus service will not response if background thread are created!!!!!!!
############################################################


################################################################
#Required !!! Override the following interface name
INTERFACE_NAME = 'com.wwjufsdatabase.collectionSyncService'



class processorThread(threading.Thread):
    def __init__(self, pendingQ):
        threading.Thread.__init__(self)
        self.pendingQ = pendingQ
    def run(self):
        ###########
        #The following are required if threads are used in the services
        gtk.gdk.threads_init()
        from dbus.mainloop.glib import threads_init
        threads_init()
        #The above lines are required if threads are used in the services
        #################
        gtk.gdk.threads_enter()
        cnt = 0
        while True:
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
            
            cnt = cnt + 1
            print cnt
        gtk.gdk.threads_leave()
        print 'returning'
    def subClassProcess(self):
        pass
        
class collectionProcessorThread(processorThread):
    def __init__(self, pendingQ, taskId, appUuid, targetRootDir, targetBackupDir, syncFolderCollectionId, 
                            collectionId, logCollectionId, workingDir, passwd):
        processorThread.__init__(self, pendingQ)
        self.syncFolderCollectionId = syncFolderCollectionId
        self.logCollectionId = logCollectionId
        self.folderPath = targetRootDir
        self.backupPath = targetBackupDir
        self.encZipPath = collectionId
        self.workingPath = workingDir
        self.passwd = passwd
        self.taskName = taskId
        self.gAppUuid = appUuid

    def subClassProcess(self):
        print 'subClassProcess called'
        
        s = advCollectionProcessor.encZipProcessor(self.taskName, self.gAppUuid, self.folderPath, self.backupPath,
                                    self.syncFolderCollectionId,
                                    transform.transformDirToInternal(self.encZipPath), 
                                    self.logCollectionId, self.workingPath, self.passwd)

        print 'start to process'
        s.process()
        
        print 'after calling subclass'

class collectionSyncService(dbusServiceBase.dbusServiceBase):
    def __init__(self, sessionBus, objectPath, appConfigDictInst = None):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        self.appConfigDictInst = appConfigDictInst
        self.pendingQ = Queue.Queue()
        self.t = None
        ###########
        #The following are required if threads are used in the services
        gtk.gdk.threads_init()
        from dbus.mainloop.glib import threads_init
        threads_init()
        #The above lines are required if threads are used in the services
        #################
        gtk.gdk.threads_enter()
        
    #The following function declaration is just a sample of dbus method
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='sssssssss', out_signature='s')
    def createSync(self, taskId, appUuid, targetRootDir, targetBackupDir, syncFolderCollectionId, 
                            collectionId, logCollectionId, workingDir, passwd):
        if self.t is None:
            self.t = collectionProcessorThread(self.pendingQ, taskId, appUuid, targetRootDir, targetBackupDir, syncFolderCollectionId, 
                            collectionId, logCollectionId, workingDir, passwd)
            if True:
                self.t.start()
            else:
                self.t.run()
            #self.startSync()
            print self.startSync()
            return "OK"
        else:
            return "Only 1 sync processor allowed"
    #The following function declaration is just a sample of dbus method
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='s')
    def startSync(self):
        print 'put item'
        self.pendingQ.put(False)
        print 'compete put'
        self.pendingQ.qsize()
        return "OK"
        
    #The following function declaration is just a sample of dbus method
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='', out_signature='s')
    def quit(self):
        print 'quitting?'
        self.pendingQ.put(True)
        return "OK"
