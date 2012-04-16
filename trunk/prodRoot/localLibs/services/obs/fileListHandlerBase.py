'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc
import os

#from pprint import pprint

import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitorQueue"
gFileListTubeName = "fileListDelayed"

gMaxZippedCollectionSize = 0.5*1024

gZipCollectionRoot = "d:/tmp/generating"

class fileListHandlerBase(object):
    '''
    classdocs
    '''
    def __init__(self, fileListTubeName = gFileListTubeName):
        '''
        Constructor
        '''
        self.fileListTubeName = fileListTubeName
        self.addedList = []

    def startServer(self):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        #beanstalk.use(self.fileListTubeName)
        beanstalk.watch(self.fileListTubeName)
        beanstalk.ignore('default')
        while True:
            job = beanstalk.reserve()
            print "got job", job.body
            item = json.loads(job.body)
            if not os.path.exists(item["fullPath"]):
                print 'Path not exists'
                job.delete()
                continue

            self.addedList.append([job, item])
            if self.processJob(job, item):
                #If processJob returns True, job processing completed, clean self.addedList
                for addedJob, addedItem in self.addedList:
                    #pprint(beanstalk.stats_tube(self.fileListTubeName))
                    #print self.addedList
                    #print dir(addedJob)
                    #print addedJob.state()
                    try:
                        addedJob.delete()
                    except:
                        pass
                    print "removed addedItem from tube", addedItem
                self.addedList = []
                
    def processJob(self, job, item):
        pass
    
    
if __name__ == "__main__":
    print 'starting fileListHandler'
    s = fileListHandlerBase()
    s.startServer()