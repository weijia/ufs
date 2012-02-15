'''
Created on 2011-10-8

@author: Richard
'''
import xmlrpclib

class launcherService(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    def launch(self, appAndParam):
        proxy = xmlrpclib.ServerProxy("http://localhost:8810/xmlrpc")
        proxy.start(appAndParam)