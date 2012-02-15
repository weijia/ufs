'''
Created on Sep 27, 2011

@author: Richard
'''
import xmlrpclib
import libSys
import libs.services.servicesV2 as service


class dbCollection(object):
    '''
    classdocs
    '''

    def __init__(self, req):
        '''
        Constructor
        '''
        self.req = req
    
    def resp(self):
        #Register to folder scanner
        self.req.resp.genHead()
        monitorRpcServerUrl = 'http://localhost:8806/xmlrpc'
        proxy = xmlrpclib.ServerProxy(monitorRpcServerUrl)
        proxy.register("D:\\sys\\pidgin\\encZip", 'http://localhost:8888/xmlrpc')
        self.req.resp.write('hello world')
        self.req.resp.genEnd()
    
if __name__=='__main__':
    dbCollection(service.req()).resp()
    
    
