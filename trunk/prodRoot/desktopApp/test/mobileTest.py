import urllib
import os

webRoot = 'http://localhost:9901'
baseDir = 'd:\\tmp\\'
dataDirBase = os.path.join(baseDir,'data')
infoDir = os.path.join(baseDir,'list.txt')

urllib.urlretrieve(webRoot+'/apps/tree/jsTreeDbNamedItem.py?id=3fe6382b-0219-40c7-add3-2f3b60aeb368', infoDir)

f = open('d:/testUrl.html')

content = f.read()

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
        
items = parseItems(content)


if not os.path.exists(dataDirBase):
    os.mkdir(dataDirBase)

for i in items.keys():
    if not os.path.exists(os.path.join(baseDir, i)):
        print '%s/apps/tree/getItemData.py?treeRoot=%s'%(webRoot, i)
        urllib.urlretrieve('%s/apps/tree/getItemData.py?treeRoot=%s'%(webRoot, i), os.path.join(dataDirBase, i))

