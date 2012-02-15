'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc


gBeanstalkdServerHost = 'localhost'
gBeanstalkdServerPort = 11300
gMonitorServiceTubeName = "monitor_queue"

class monitorService(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    def addItem(self, fullPath):
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(gMonitorServiceTubeName)
        job = beanstalk.put('{"fullPath":"'+fullPath+'"}')
        