import logging
import logging.config
from twisted.web import proxy

logging.config.fileConfig("logging.conf")

#create logger
logger = logging.getLogger("basicLog")

def printLog(*args):
    logStr = ''
    for i in args:
        logStr += str(i)
    logger.debug(logStr)
    
def formatHeader(header):
    words = header.split('-')
    newWords = []
    for i in words:
        newWords.append(i.capitalize())
    return '-'.join(newWords)

class correctHeaderProxyClient(proxy.ProxyClient):
    def connectionMade(self):
        #Need to change headers to be more standard
        for header, value in self.headers.items():
            del self.headers[header]
            self.headers[formatHeader(header)] = value
            #printLog('-'.join(newWords),value)
        printLog('connected to server')
        proxy.ProxyClient.connectionMade(self)
        printLog('connectionMade function called')
