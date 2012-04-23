'''
Created on 2011-9-22

@author: Richard
'''

import localLibSys
from localLibs.logSys.logSys import *
import threading
import time
import beanstalkc
import wwjufsdatabase.libs.utils.simplejson as json
import xmlrpclib

gXmlRpcServerPort = 8909
#gXmlRpcServerUrl = u"http://127.0.0.1:%d/xmlrpc"%gXmlRpcServerPort
gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = 11300


import xmlRpcServerBase

def subscribe(tube_name):
    proxy = xmlrpclib.ServerProxy("http://localhost:%d/xmlrpc"%gXmlRpcServerPort)
    #argv1 task id, argv2 passwd
    res = proxy.subscribe(tube_name)
    print res

class XmlRpcServer2BeanstalkdServiceBridge(xmlRpcServerBase.managedXmlRpcServerBase):
    '''
    classdocs
    
    '''
    def __init__(self, port):
        super(XmlRpcServer2BeanstalkdServiceBridge, self).__init__(port)
        self.beanstalkd_service_command_tube_names = []
        self.beanstalk = None
        
    def get_beanstalkd_instance(self):
        if self.beanstalk is None:
            self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        return self.beanstalk

        self.beanstalk.ignore('default')
    def subscribe(self, beanstalkd_tube_name):
        self.beanstalkd_service_command_tube_names.append(beanstalkd_tube_name)
        return "added: "+beanstalkd_tube_name
        
    subscribe.exposed = True
    def stop(self):
        #Send messages to all beanstalkd service
        for i in self.beanstalkd_service_command_tube_names:
            self.get_beanstalkd_instance().use(i)
            item_dict = {"command": "quit"}
            s = json.dumps(item_dict, sort_keys=True, indent=4)
            print "add item:", s, i
            job = self.beanstalk.put(s, priority = 1000)
    stop.exposed = True
    
if __name__ == '__main__':
    # Set up site-wide config first so we get a log if errors occur.
    xmlRpcServerBase.startMainServer(XmlRpcServer2BeanstalkdServiceBridge(gXmlRpcServerPort))