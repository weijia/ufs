from cherrypy import _cptools
import cherrypy
import Queue
import localLibSys
import localLibs.localTasks.advCollectionProcessorV2 as advCollectionProcessor
import wwjufsdatabase.libs.utils.transform as transform
import threading

class Root:
    def index(self):
        return "I'm a standard index!"
    index.exposed = True

    
class processorThread(threading.Thread):
    def __init__(self, pendingQ):
        threading.Thread.__init__(self)
        self.pendingQ = pendingQ
    def run(self):
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

    
    
class syncServiceServer(_cptools.XMLRPCController):
    def __init__(self):
        _cptools.XMLRPCController.__init__(self)
        self.pendingQ = Queue.Queue()
        self.t = None
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
            print self.startSync()
            return "Only 1 sync processor allowed"
    createSync.exposed = True
        
    def startSync(self):
        print 'put item'
        self.pendingQ.put(False)
        print 'compete put'
        self.pendingQ.qsize()
        return "OK"
    startSync.exposed = True


if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    root = Root()
    root.xmlrpc = syncServiceServer()

    cherrypy.config.update({'environment': 'production',
                            'log.error_file': '../../../../site.log',
                            'log.screen': True,
                            'engine.autoreload_on' : True,
                            'server.socket_port' : 8806,
                            'request.dispatch': cherrypy.dispatch.XMLRPCDispatcher(),
                            'tools.xmlrpc.allow_none': 1,})

    cherrypy.quickstart(root, '/')    
