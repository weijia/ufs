import libSys
import urllib
import libs.html.response
import libs.http.queryParam
import os
from desktopApp.lib.transform import *
import collectionV8 as collection

import collectionIteratorV2
from desktopApp.lib.transform import *

#import shove
import libs.cache.encryptedShove as shove
import uuid


gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')

def fileIter(fullPath):
    for i in os.listdir(fullPath):
        try:
            p = os.path.join(fullPath, i)
            if not os.path.isdir(p):
                yield i.decode("gb2312")
        except UnicodeDecodeError:
            continue


libs.utils.misc.ensureDir(gDbPath)

def collectionWithPreview(htmlGen, fullPath, page):
    collectionPreviewPathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewPathDb.sqlite'))
    collectionPreviewUuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'collectionPreviewUuidDb.sqlite'))
    #htmlGen.write('<div style="white-space:nowrap">')
    h=htmlGen
    try:
        u = collectionPreviewPathDb[fullPath]
    except KeyError:
        u = str(uuid.uuid4())
        collectionPreviewPathDb[fullPath] = u
        collectionPreviewUuidDb[u] = fullPath
    #h.write(fullPath)
    iter = fileIter(fullPath)
    i = collectionIteratorV2.cachedCollectionIter(u, iter, 0)
    #h.write(fullPath)
    h.write('<div style="float:left;max-width:30%">')
    h.write('<div style="float:left;min-width:25%">')
    co = []
    #h.write(fullPath)
    for k in i:
        p = transformDirToInternal(os.path.join(fullPath, k))
        #h.write(k+'<br/>')
        co.append([p, p])
    #h.write(str(co))
    #h.write(fullPath)

    collection.showCollection(htmlGen, co, fullPath, None)
    h.write('</div>')
    if True:
        h.inc('/webapproot/js/custom/editable.js')
        h.inc('/webapproot/js/pageScript/collectionWithPreviewV8.js')
    htmlGen.write('</div>')
    htmlGen.write('<div style="white-space:nowrap">')
    htmlGen.write('''
        <img id="previewImage" style="max-width:500px;"/>
    ''')
    htmlGen.write('</div>')
    #htmlGen.write('<div id="log"/>')

if __name__=='__main__':
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]    
    page = int(fields.get("page",[0])[0])
    thumbPerLine = int(fields.get("thumbPerLine", [5])[0])
    #print 'calling album'
    #i = albumIterator(path)
    #print 'after calling'
    h = libs.html.response.html()
    h.genHead('Collections')
    collectionWithPreview(h, path, page)
    h.genEnd()
