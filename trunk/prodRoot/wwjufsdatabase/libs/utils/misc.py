import os

def ensureDir(fullPath):
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)

        
        
gSupportedExt = ['jpg','avi']

def withExt(fullPath, extList = gSupportedExt):
    s = fullPath.split('.')
    if len(s) > 1:
        if  s[-1].lower() in extList:
            #print fullPath, extList
            return True
    return False
