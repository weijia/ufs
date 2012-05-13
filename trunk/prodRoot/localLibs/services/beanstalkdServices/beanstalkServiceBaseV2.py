'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import traceback
import threading
import sys

import localLibSys
#from localLibs.windows.changeNotifyThread import changeNotifyThread
import wwjufsdatabase.libs.utils.simplejson as json
#import localLibs.server.XmlRpcServer2BeanstalkdServiceBridge as bridge

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gItemDelayTime = 60*60*24#One day
g_stop_msg_priority = 2**30

class beanstalkServiceBase(object):
    '''
    classdocs
    '''
    def __init__(self, tube_name = None):
        '''
        Constructor
        '''
        if tube_name is None:
            tube_name = self.__class__.__name__ + "_default_cmd_tube_name"
        self.tubeName = tube_name
        self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
    
    def put_item(self, item_dict, target_tube, priority = beanstalkc.DEFAULT_PRIORITY):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(target_tube)
        s = json.dumps(item_dict, sort_keys=True, indent=4)
        print "add item:", s, self.tubeName
        job = beanstalk.put(s, priority = priority)
        return job
    
    def addItem(self, itemDict, priority = beanstalkc.DEFAULT_PRIORITY):
        return self.put_item(itemDict, self.tubeName, priority)
        
    def watchTube(self):
        print 'watch tube: ', self.tubeName
        self.beanstalk.watch(self.tubeName)
        self.beanstalk.watch(self.tubeName+"_stop_tube")
        self.beanstalk.ignore('default')
        
    def is_term_signal(self, item):
        if item.has_key("cmd"):
            if item["cmd"] == "stop":
                print "got a quit message"
                return True
        return False
    
    def processItem(self, job, item):
        job.delete()
        return False#Return False if we do not need to put the item back to tube
    
    def stop(self):
        print "got a quit message"

gBeanstalkdLauncherServiceTubeName = "beanstalkd_launcher_service"


class beanstalkServiceApp(beanstalkServiceBase):
    def __init__(self, tube_name = None):
        super(beanstalkServiceApp, self).__init__(tube_name)
        #bridge.subscribe(tube_name)
        ##############################
        # The thread should be value not the key in taskDict
        ##############################
        self.taskDict = {}

    def register_cmd_tube(self):
        pid = os.getpid()
        print "current pid: ", pid
        
        #self.put_item({"cmd": "registration", "pid": pid, 
        #               "cmd_tube_name": self.tubeName}, gBeanstalkdLauncherServiceTubeName)
        self.put_item({"cmd": "registration", "pid": pid, 
                       "cmd_tube_name": self.tubeName+"_stop_tube"}, gBeanstalkdLauncherServiceTubeName)
        
    def startServer(self):
        print self.__class__, self.tubeName
        self.register_cmd_tube()
        self.watchTube()
        #!!!Not working. Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        while True:
            try:
                job = self.beanstalk.reserve()
            except:
                self.stop()
                return
            print "got job", job.body
            item = json.loads(job.body)
            if self.is_term_signal(item):
                self.stop()
                job.delete()
                return
                #continue
            print item
            try:
                if self.processItem(job, item):
                    #If return True, the job was processed but should be still in queue, release and delay it
                    job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
                ########################################
                # !!! Otherwise, sub class must delete the item. Or timeout will occur
                ########################################
            except Exception,e:
                print >>sys.stderr, "processing task error, ignore the following"
                traceback.print_exc()
                #raise e
                job.delete()
                
    def stop(self):
        #Tell all sub process to stop
        for i in self.taskDict:
            self.put_item({"cmd": "stop"}, self.taskDict[i], g_stop_msg_priority)

class beanstalkWorkingThread(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, inputTubeName):
        super(beanstalkWorkingThread, self).__init__(inputTubeName)
        threading.Thread.__init__(self)
        
    def run(self):
        self.startServer()
        
    def stop(self):
        pass
        
if __name__ == "__main__":
    s = beanstalkServiceBase()
    s.startServer()