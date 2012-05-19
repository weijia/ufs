import socket

import configurationTools as config
import transform
import localLibSys
from localLibs.logSys.logSys import *


gUfsObjUrlPrefix = u'ufsFs'+config.getFsProtocolSeparator()
gUfsObjUrlSeparator = u'/'


def parseUrl(url):
    return url.split(config.getFsProtocolSeparator(),2)
    


def getHostName():
    return unicode(socket.gethostname())

def getUfsUrlForPath(fullPath):
    fullPath = transform.transformDirToInternal(fullPath)
    return gUfsObjUrlPrefix + getHostName() + gUfsObjUrlSeparator + fullPath
       
def getFullPathFromUfsUrl(ufsUrl):
    if not isUfsFs(ufsUrl):
        cl(ufsUrl)
        raise "not ufs url"
    objPath = parseUrl(ufsUrl)[1]
    hostname, fullPath = objPath.split(gUfsObjUrlSeparator, 1)
    #print hostname, fullPath
    if unicode(hostname) != getHostName():
        raise 'not a local file'
    return fullPath


def isUuid(url):
    return (url.find(u"uuid"+config.getFsProtocolSeparator()) == 0)

def getUrlContent(url):
    protocol, content = parseUrl(url)
    return content
    
def getPathForUfsUrl(url):
    url_content = getUrlContent(url)
    return url_content.split(gUfsObjUrlSeparator, 1)[1]
    
def getUuid(url):
    return getUrlContent(url)
    
def getUrlForUuid(id):
    return u"uuid"+config.getFsProtocolSeparator()+id
    
def isUfsUrl(url):
    '''
    In format of xxxx://xxxx
    '''
    if url.find(config.getFsProtocolSeparator()) == -1:
        return False
    else:
        return True
        
def getUfsUrl(localPath):
    return gUfsObjUrlPrefix+getHostName()+gUfsObjUrlSeparator+transform.transformDirToInternal(localPath)

def getUfsLocalRootUrl():
    return gUfsObjUrlPrefix+getHostName()+gUfsObjUrlSeparator
    
def isUfsFs(url):
    return (url.find(gUfsObjUrlPrefix) == 0)

def getUfsBasename(url):
    return url.rsplit(gUfsObjUrlSeparator, 1)[1]


