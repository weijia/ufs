import os
import sys
#from logSys import *

localStringEncoding = 'gb2312'

def transformLocalStringToUnicode(originalString):
    '''
    Transform a string in local format to unicode. This may be changed in different
    system as different system has different default encoding
    '''
    if type(originalString) != unicode:
        return originalString.decode(localStringEncoding)
    return originalString
  #return originalString

def transformUnicodeStringToLocal(originalString):
    '''
    Transform a string in local format to unicode. This may be changed in different
    system as different system has different default encoding
    '''
    return originalString.encode(localStringEncoding)
  #return originalString

def formatRelativePath(relativePath):
    '''
    Transform dir to internal format.
    In windows, it will be like: D:/helloworld.txt
      The driver letter D should be capitalized. Separator should be '/' instead of '\\'
    
    The input should be unicode. Anyway, we'll check it in this function.
    
    '''
    newDir = transformLocalStringToUnicode(relativePath)
    newDir = newDir.replace(u'\\', u'/')
    '''
    if newDir[0] == u'/':
        newDir = newDir[1:]
    '''
    #Remove trail '/'
    newDir = newDir.rstrip(u'/')
    return newDir


def transformDirToInternal(originalDir):
    '''
    Transform dir to internal format.
    In windows, it will be like: D:/helloworld.txt
      The driver letter D should be capitalized. Separator should be '/' instead of '\\'
    
    The input should be unicode. Anyway, we'll check it in this function.
    
    '''
    newDir = transformLocalStringToUnicode(os.path.abspath(originalDir))
    #print type(newDir)
    if sys.platform == 'win32':
        #In windows, make the driver letter upper case
        if newDir[1] == u':':
            newDir = newDir[0].upper() + newDir[1:]
        else:
            cl('not a correct directory format in windows. Dir is:', newDir)
    newDir = newDir.replace(u'\\',u'/')
    #ncl(newDir)
    #TODO: support linux path?
    #Remove trail '/'
    #print newDir
    newDir = newDir.rstrip(u'/')
    if sys.platform == 'win32':
        #In windows, make the driver letter upper case
        if len(newDir) == 2:
            #C: or E:
            newDir = newDir + u"/"
    return newDir

def getRelativePathFromFull(fullPath, rootPath):
    rootPath = transformDirToInternal(rootPath)
    if rootPath[-1] != u"/":
        rootPath += u"/"
    return transformDirToInternal(fullPath).replace(rootPath, "")

def autoDecoder(orig):
    '''
    shall decode the string to unicode
    '''
    return orig
