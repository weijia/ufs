import urllib
import os

webRoot = 'http://localhost:9901'
# baseDir = 'd:\\tmp\\'
# dataDirBase = os.path.join(baseDir,'data')
# infoDir = os.path.join(baseDir,'list.txt')
#infoDir = 'list.txt'

def parseItems(content):
    c = content.split('-->')
    r = ''
    for i in c:
        m = i.split('<!--')
        if len(m) < 2:
            #No comment
            #print m
            r += m[0]
        else:
            #One comment
            #print m
            #print len(m), ''.join(m[0:-1])
            r += ''.join(m[0:-1])
    #print 'removed comments:',r

    r = r.replace('\r','')
    r = r.replace('\n','')
    l = r.split('</li>')
    #print l
    items = {}
    import re
    for i in l:
        if i == '':
            continue
        m1 = re.search('id=\"([0-9a-f\-]+)\"',i)
        m2 = re.search('</ins>([^<]+)</a>',i)
        items[m1.groups(0)[0]] = m2.groups(0)[0]
        #print m1.groups(0)[0]
        #print m2.groups(0)[0]
    return items



def getItemList(itemAbsPath, tmpPath):
    infoPath = os.path.join(tmpPath, 'namedTreeItemList.txt')
    urllib.urlretrieve(webRoot+'/apps/tree/jsTreeDbNamedItem.py?id=%s'%itemAbsPath, infoPath)
    f = open(infoPath)
    items = parseItems(f.read())
    f.close()
    return items


def downloadItem(itemId, itemName, destPath):
    print 'Download:%s,%s'%(itemId, itemName)
    dataPath = os.path.join(destPath, itemName)
    urllib.urlretrieve(webRoot+'/apps/tree/getItemData.py?treeRoot=%s'%itemId, dataPath)

def downloadStorage(itemId, itemName, destPath):
    print 'Download:%s,%s'%(itemId, itemName)
    dataPath = os.path.join(destPath, itemName)
    urllib.urlretrieve(webRoot+'/apps/tree/getStorageData.py?storageId=%s'%itemId, dataPath)
    
def getStorageId(itemId, tmpPath):
    dataPath = os.path.join(tmpPath, 'tmp.txt')
    urllib.urlretrieve(webRoot+'/apps/tree/getItemDataId.py?treeRoot=%s'%itemId, dataPath)
    f = open(dataPath)
    a = f.read()
    f.close()
    return a
