import os
import re

def findFileInProduct(filename):
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        if filename in filenames:
            #print 'find file:', os.path.join(dirpath, filename)
            return os.path.join(dirpath, filename)
    return None

def findNamePatternInProduct(pattern):
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        for i in filenames:
            res = re.search(pattern, i)
            #print pattern, i
            if res is None:
                continue
            #print 'found item:', pattern, i
            return os.path.join(dirpath, i)
    return None


def findAppInProduct(filename):
    #filename = filename.replace('-', '\-')
    return findNamePatternInProduct(filename+"((\.bat)|(\.py)|(\.exe)|(\.com))")