import libSys
import libs.html.response
import libs.platform.services
import os
import shove
import libs.thumb.picThumbGenerator
from desktopApp.lib.transform import *
import uuid

gAppPath = 'd:/tmp/fileman/'
gDbPath = os.path.join(gAppPath, 'db')
gThumbPath = os.path.join(gAppPath, 'thumb')

def ensureDir(fullPath):
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)
        
ensureDir(gAppPath)
ensureDir(gDbPath)
ensureDir(gThumbPath)

lengthDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'lengthDb.sqlite'))
#treeDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'treeDb.sqlite'))
thumbDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'thumb.sqlite'))
pathDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'pathDb.sqlite'))
uuidDb = shove.Shove('sqlite:///'+os.path.join(gDbPath,'uuidDb.sqlite'))


def show_file(path):
    import serve_file
    files = serve_file.file_request_handler()
    path = transformDirToInternal(path)
    try:
        u = pathDb[path]
    except KeyError:
        u = str(uuid.uuid4())
        pathDb[path] = u
        uuidDb[u] = path
    try:
        newPath = thumbDb[u]
    except:
        newPath = libs.thumb.picThumbGenerator.genPicThumb(path, gThumbPath)
        thumbDb[u] = newPath
        #thumbFile = libs.thumb.picThumbGenerator.returnThumbString(path)
        #files.serveStringFile(thumbFile, path)
        #files.serve(path)
    files.serve(newPath)

  
def show_dir():
    fields = libs.http.queryParam.queryInfo().getAllFieldStorage()
    path = fields["path"][0]
    if not os.path.isdir(path):
        show_file(path)
    else:
        for name in os.listdir(path):
            s = name.split('.')
            if len(s) > 1:
                if  s[1] == 'jpg':
                    show_file(os.path.join(path, name))
                    break
                
if __name__=='__main__':
    show_dir()