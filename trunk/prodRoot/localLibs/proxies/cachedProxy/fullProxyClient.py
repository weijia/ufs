#from shove import Shove
import os
from url2name import *
#from toollibs import *
#from logSys import *
#from databaseSys import *
#cacheBase = 'd:/cache/'

from twisted.web import proxy
'''
from filesystemManager import *
fs = filesystemManager()
'''
#from dummyProxyClientFactory import *

#from proxyClientWithTimer import *

#from tools import *
        
HAS_DATA_RETRY = 20
NO_DATA_RETRY = 6


from localLibs.logSys.logSys import *

#class fullProxyClient(proxyClientWithTimer):
class fullProxyClient(proxy.ProxyClient):
    '''
    self.info['ext']: used to generate the cache file extension.
    self.info['headersOrdered']: used when replay headers to client. The order received from server will not be changed.
    self.info['headers']: used to store headers, headers key must be stored in lowcase
    self.info['totoalLen']: total length of the URL object, part range responsed length is small than this length
    self.info['parts']['start']: data range response's start position
    self.info['parts']['curPos']: current start position of un received data in the cache
    self.info['parts']['partLen']: data range response's length. It will be always <= self.info['totalLen']
    '''
    '''
    This class is used to handle content returned by web server
    '''
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
    def removeHeader(self, key):
        try:
            del self.info['headers'][key]
        except:
            pass
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
        proxy.ProxyClient.handleStatus(self, version, code, message)
    def handleEndHeaders(self):
        if self.validStatus():
            cl('handle end of header')
            
            #Handle range info and size info
            if self.info['headers'].has_key('content-length'):
                if not self.rangeFlag:
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
            self.info['ext'] = genExtFromHeaders(self.info['headers'])
            self.saveInfo()

            #Delete the following headers so they will not affecting endHeader processing
            self.removeHeader('content-range')
            self.removeHeader('content-length')

        #proxyClientWithTimer.handleEndHeaders(self)
        #self.smartClientFactory.handleEndHeaders()
        #Why we do not re-connect again? Remove it
        #self.doNotReconnectAgain = True
        proxy.ProxyClient.handleEndHeaders(self)
        
    def writeData(self, curPos, data):
        cachePath = url2name.url2dir(self.uri, self.proxyParam["cacheRootPath"])
        #Write data write log
        #cl('id:',self.id,'data received')
        o = open(os.path.join(cachePath,'log.txt'),'ab')
        print >>o, 'write at',curPos,'len:',len(data),'\r\n'
        o.close()
        #Update the real data
        f = open(os.path.join(cachePath,'content'+ self.client.info['ext']),'ab')#use ab, so will not truncate the file.
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
        self.father.transport.write(data)
        self.writtenDataLength += len(data)
        cl('id:',self.id,',', self.writtenDataLength, ',written')
        
    def handleHeader(self, key, value):
        #Do we need to remove 'content-length' and 'content-range' here before calling parent class function?
        #Will these 2 be sent directly in this function? From twisted code, no.
        #So we can delete them in endHeader
        #proxyClientWithTimer.handleHeader(self, key, value)
        self.handleHeader(key, value)
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
            
    def handleResponsePart(self, data):
        '''
        This function will be called when http response data got.
        Handle the data of the request
        '''
        if self.validStatus():
            self.smartClientFactory.writeData(self.info['parts']['curPos'], data)
            self.info['parts']['curPos'] += len(data)#This position is the pos for this client request
            ncl('id:', self.proxyParam["curId"],',return from handle response part')
            self.saveInfo()


    def handleResponseEnd(self):
        '''
        This is called when the response data is totally received
        '''
        #proxyClientWithTimer.handleResponseEnd(self)
        #If handling ranging, do not save info at this point?
        if self.rangeFlag:
            #Range accept, send the first part of the data.
            cachePath = url2dir(self.uri, 'd:/cache/')
            data = open(os.path.join(cachePath, 'content'+ self.filenameExt), 'rb').read()
            #self.smartClientFactory.writeRealData(data)
        elif self.validStatus():
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
        import pickle
        pickle.dump(self.info, db)
        db.close()
        hdF = open(os.path.join(self.path,'headers.txt'),'wb')
        for i in self.info['headers'].keys():
            print >>hdF, '%s: %s'%(i, self.info['headers'][i])
        hdF.close()
        #print 'write header completed',os.path.join(self.path,'headers.txt')

    def timeoutAction(self):
        print 'timeout action, uri:',self.smartClientFactory.uri
        self.reconnectServer()
    

    def connectionMade(self):
        self.doNotReconnectAgain = False
        #Set father's connection lost notification callback
        self.father.connectionLostCallback = self.clientDisconnected
        self.retry = NO_DATA_RETRY
        self.filenameExt = ''
        self.rangeFlag = False
        #Connection established, load info
        self.path = url2dir(self.smartClientFactory.uri)
        try:
            db = open(os.path.join(self.path,'objDb.cpickle'),'rb')
            import pickle
            self.info = pickle.load(db)
            db.close()
            if self.validStatus():
              #Connected to server, check if loaded info is OK and generate range request.
              if self.info['parts'].has_key('curPos') and (self.info['parts']['curPos']>0):
                  if (not self.info.has_key('totalLen')) or \
                      self.info['parts']['curPos'] < self.info['totalLen']:
                      #cur pos < total len, so range request needed. May check if server accept range request in the future
                      self.headers['Range'] = 'bytes=' + str(self.info['parts']['curPos']) +'-'
                      cl('sending range, Range: ',self.headers['Range'])
              cl('-------------------load successfully')
              
              #save old header info, so they will not affecting endHeader processing
              self.info['lastHeaders'] = self.info['headers']
              self.info['headers'] = {}
              print self.info['lastHeaders']
              '''
              #Delete the following headers so they will not affecting endHeader processing
              self.removeHeader('content-range')
              self.removeHeader('content-length')
              '''
        except IOError:
            self.info = {}
            self.info['headers'] = {}
            self.info['headersOrdered'] = []
            self.info['reloadCnt'] = 0
        self.info['parts'] = {}
        self.info['parts']['curPos'] = 0
