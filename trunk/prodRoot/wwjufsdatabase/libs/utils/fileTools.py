import os
import time
import random

def getFreeName(path, nameWithoutExt, ext):
    path_without_ext = os.path.join(path, nameWithoutExt)
    while os.path.exists(path_without_ext+ext):
        path_without_ext += '-' + str(random.randint(0,10))
        #print thumb_path_without_ext
    return path_without_ext+ext

def getFreeNameFromFullPath(fullPath):
    path = os.path.dirname(fullPath)
    ext = os.path.splitext(fullPath)[1]
    basename = os.path.basename(fullPath)
    #print basename
    nameWithoutExt = basename[0:-(len(ext))]
    #print nameWithoutExt
    if nameWithoutExt == '':
        nameWithoutExt = basename
        ext = ''
    res = getFreeName(path, nameWithoutExt, ext)
    #print res
    return res
  
def getTimestampWithFreeName(path, ext, prefix = ''):
    filename = unicode(prefix + str(time.time()))
    return getFreeName(path, filename, ext)
    