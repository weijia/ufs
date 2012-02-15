'''
Created on Oct 15, 2011

@author: Richard
'''
import urlparse
import os
from twisted.web import proxy
import pickle


import localLibSys
import localLibs.proxies.proxyBaseClass.proxyFrameworkV4 as proxyFramework
import localLibs.proxies.proxyBaseClass.proxyAppBaseV3 as proxyAppBase
import localLibs.proxies.proxyBaseClass.advProxyFrameworkV2 as advProxyFramework
from localLibs.logSys.logSys import *
import proxyTools
import url2name


class recordedProxyClient(advProxyFramework.proxyClientWithParam):
    def handleStatus(self, version, code, message):
        cl('handle state id:', self.proxyParam["curId"], version, code, message)
        #proxyClientWithTimer.handleStatus(self, version, code, message)
        self.info['status'] = {}
        self.info['status']['version'] = version
        self.info['status']['code'] = code
        self.info['status']['message'] = message
        #import exception
        try:
            if int(code) == 206:
                cl('--------------------range request accepted')
                self.rangeFlag = True
        except ValueError:
            self.info['status']['code'] = 500
        #self.smartClientFactory.handleStatus(version, code, message)
        super(recordedProxyClient, self).handleStatus(self, version, code, message)
    def validStatus(self):
        '''
        Check if status code is OK, if not OK return False, then system will not cache the page
        '''
        try:
            if (int(self.info['status']['code']) == 206) or (int(self.info['status']['code']) == 200):
                return True
        except:
            pass
        return False
    
    def writeData(self, curPos, data):
        cachePath = self.path
        #Write data write log
        #cl('id:',self.id,'data received')
        o = open(os.path.join(cachePath,'log.txt'),'ab')
        print >>o, 'write at',curPos,'len:',len(data),'\r\n'
        o.close()
        #Update the real data
        f = open(os.path.join(cachePath,'content'+ self.info['ext']),'ab')#use ab, so will not truncate the file.
        f.seek(curPos)
        f.write(data)
        cl('writing:', cachePath,'curP:',curPos)
        f.close()
        #Send proper data to client
        if self.writtenDataLength > curPos:
            off = self.writtenDataLength - curPos
            if off < len(data):
                self.writeRealData(data[off:])
        elif self.writtenDataLength == curPos:
            self.writeRealData(data)
        else:
            cl('id:', self.proxyParam["curId"], 'cur:%d, got:%d'%(self.writtenDataLength,curPos))
            
    def writeRealData(self, data):
        self.father.write(data)
        self.writtenDataLength += len(data)
        cl('id:', self.proxyParam["curId"],',', self.writtenDataLength, ',written')
    
    def handleResponsePart(self, data):
        '''
        This function will be called when http response data got.
        Handle the data of the request
        '''
        if self.validStatus():
            self.writeData(self.info['parts']['curPos'], data)
            self.info['parts']['curPos'] += len(data)#This position is the pos for this client request
            ncl('id:', self.proxyParam["curId"],',return from handle response part')
            self.saveInfo()


    def handleResponseEnd(self):
        '''
        This is called when the response data is totally received
        '''
        #proxyClientWithTimer.handleResponseEnd(self)
        #If handling ranging, do not save info at this point?
        '''
        if self.rangeFlag:
            #Range accept, send the first part of the data.
            cachePath = url2name.url2dir(self.uri, self.proxyParam["cacheRootPath"])
            data = open(os.path.join(cachePath, 'content'+ self.filenameExt), 'rb').read()
            #self.smartClientFactory.writeRealData(data)
        '''
        if self.validStatus():
            '''
            Server returned valid status, save all headers and generated infos
            '''
            cl('id:', self.proxyParam["curId"],'response end')
            self.saveInfo()

            #Do extra check to see if all data received
            if self.info.has_key('totalLen'):
                if int(self.info['parts']['curPos']) != int(self.info['totalLen']):
                    cl('not match: real:%d, expected:%d'%(self.info['parts']['curPos'],\
                        int(self.info['parts']['totalLength'])))
                    #self.doNotReconnectAgain = False#Remove this, as no one will set it to True unless someone want it to be True.
                    self.reconnectServer()
                else:
                    ncl('match: real:%d, expected:%d'%(self.info['parts']['curPos'],\
                        int(self.info['parts']['totalLength'])))
            else:
                cl('no total length got, set totalLen to received length')
                self.info['parts']['totalLen'] = self.info['parts']['curPos']
            cl("id", self.proxyParam["curId"],'handle respose end called')
    def saveInfo(self):
        db = open(os.path.join(self.path,'objDb.cpickle'),'wb')
        #print 'writing cpickle',os.path.join(self.path,'objDb.cpickle')
        
        pickle.dump(self.info, db)
        db.close()
        hdF = open(os.path.join(self.path,'headers.txt'),'wb')
        for i in self.info['headers'].keys():
            print >>hdF, '%s: %s'%(i, self.info['headers'][i])
        hdF.close()
    def handleHeader(self, key, value):
        #Do we need to remove 'content-length' and 'content-range' here before calling parent class function?
        #Will these 2 be sent directly in this function? From twisted code, no.
        #So we can delete them in endHeader
        #proxyClientWithTimer.handleHeader(self, key, value)
        advProxyFramework.proxyClientWithParam.handleHeader(self, key, value)
        self.info['headers'][key.lower()] = value
        ncl('id:', self.proxyParam["curId"], 'header received:',key, value)
        #Add header order info, so it can be replayed
        try:
            self.info['headersOrdered'].index(key)
        except ValueError:
            self.info['headersOrdered'].append(key)
            
        if self.validStatus():
            #self.saveInfo()#Do we need to save the heads for each? Just save it when endHeaders now
            pass
    def handleEndHeaders(self):
        if self.validStatus():
            cl('handle end of header')
            #Handle range info and size info
            ''
            if self.info['headers'].has_key('content-length'):
                #if not self.rangeFlag:
                if True:
                    #When not range response, totoal length is equal to content-length
                    self.info['parts']['totalLength'] = int(self.info['headers']['content-length'])#For compatibility, may be removed in the future, use self.info['totoalLen']
                    self.info['totoalLen'] = int(self.info['headers']['content-length'])
            if self.info['headers'].has_key('content-range'):
                value =  self.info['headers']['content-range']
                cl('-----------------------Get range:',value)
                try:
                    start = int(value.split(' ')[1].split('-')[0])
                except ValueError:
                    #The content-range: */1234 situation
                    start = self.info['parts']['curPos']
                total = int(value.split(' ')[1].split('/')[1])
                self.info['parts']['curPos'] = start
                self.info['parts']['start'] = start
                self.info['parts']['totalLength'] = total#For compatibility, may be removed in the future, use self.info['totoalLen']
                self.info['totoalLen'] = total
                #The following is an extra check, the following check should be always OK.
                if self.info['parts']['totalLength'] != int(self.info['parts']['start']) + \
                        int(self.info['headers']['content-length']):
                    print 'range returned value is not correct!!!!!!'
                    
            #Generate cache extension for local file
            self.info['ext'] = proxyTools.genExtFromHeaders(self.info['headers'])
            self.saveInfo()

            #Delete the following headers so they will not affecting endHeader processing
            #self.removeHeader('content-range')
            #self.removeHeader('content-length')
        
    def connectionMade(self):
        cl("connecting ", self.father.uri)
        advProxyFramework.proxyClientWithParam.connectionMade(self)
        self.info = {}
        self.path = url2name.url2dir(self.father.uri, self.proxyParam["cacheRootPath"])
        self.info['headers'] = {}
        self.info['headersOrdered'] = []
        self.info['reloadCnt'] = 0
        self.info['parts'] = {}
        self.info['parts']['curPos'] = 0
        self.writtenDataLength = 0
        
if __name__ == "__main__":
    param = {"proxyRequestFactoryClass": proxyFramework.proxyRequestFactory,
             "proxyRequestClass": advProxyFramework.proxyRequestCreatingClientFactoryWithParam,
             "proxyClientFactoryClass": advProxyFramework.proxyClientFactoryWithParam,
             "proxyClientClass": recordedProxyClient,
             "servePort":8809,
             "curId": 0,
             "cacheRootPath": "d:/tmp/"
        }
    a = proxyAppBase.proxyAppBase(param)
    a.createProxyStart()
