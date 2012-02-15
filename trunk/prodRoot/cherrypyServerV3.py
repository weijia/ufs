import os.path
import cherrypy
from cherrypy.lib.static import serve_file
#import sqlite3
import wwjufsdatabase.libs.thumb.thumbInterface as thumbLib
#from desktopApp.lib.transform import *
import uuid
import logging
#import pymedia.muxer
import os
import wwjufsdatabase.libs.utils.misc as misc
import wwjufsdatabase.libs.utils.encodingTools as encodingTools
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.ufsDb.ufsDbSingleUser as ufsDbSingleUser

gAppPath = 'd:/tmp/fileman/'
gThumbPath = os.path.join(gAppPath, 'thumb')

misc.ensureDir(gAppPath)
misc.ensureDir(gThumbPath)

#import wwjufsdatabase.libs.shove.shoveClientV5 as shoveClient
#thumbDb = libs.cache.shoveClient.Shove()

class simpleSysUser:
    def getUserName(self):
        return 'system.default'
    def getPasswd(self):
        return 'simplePass'


def getProdRoot():
    c = os.getcwd()
    while c.find('prodRoot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'prodRoot')


class Root:
    def __init__(self):
        sessInst = simpleSysUser()
        dbSysInst = ufsDbSingleUser.dbSysSmart(sessInst)

        self.thumbDb = dbSysInst.getDb('thumbNew')
        self.pathDb = dbSysInst.getDb('pathNew')
        self.uuidDb = dbSysInst.getDb('uuidNew')
        self.existingIconRelativePath = 'wwjufsdatabase\\webapproot\\static\\icons\\'
        self.prodRootPath = getProdRoot()
        
    @cherrypy.expose
    def thumb(self, path):
        #print path
        thumbP = self.getThumb(path)
        #print thumbP
        if thumbP is None:
            return None
        ext = thumbP.split('.')[-1]
        typeMapping = {'jpg':'image/jpeg', 'jpeg':'image/jpeg', 'png':'image/png', 'bmp':'image/bmp'}
        t = typeMapping[ext]
        return serve_file(thumbP,content_type=t)
        
    def getThumb(self, fullPath):
        path = transform.transformDirToInternal(fullPath)
        if not os.path.exists(path):
            print path.encode("gbk", "replace"), " not exist"
            raise KeyError
        try:
            u = unicode(self.pathDb[path][0])
        except KeyError:
            u = unicode(uuid.uuid4())
            self.pathDb[path] = u
            self.uuidDb[u] = path
        newPath = None
        try:
            #raise "no"
            newPath = self.thumbDb[u][0]
        except KeyError:
            #print path
            if os.path.isdir(path):
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'folder-images-icon.png')
            ext = path.split('.')[-1].lower()
            newPath = thumbLib.getThumb(path, gThumbPath)
            if not (newPath is None):
                return newPath
            sup = ['doc','zip','wav','xls','txt','rar', 'pdf', 'ppt']
            picSup = ['flv','mov','avi','rm','rmvb','jpg','jpeg','png','gif','bmp','wmv','mp4','3gp','mpg','mpeg', 'exe']

            if ext in sup:
                #print os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\%s.png'%ext)
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\%s.png'%ext)
            if not (ext in picSup):
                #print os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
            newPath = thumbLib.getThumb(path, gThumbPath)
            if newPath is None:
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
            newPath = transform.transformDirToInternal(newPath)
            self.thumbDb[u] = newPath
            #thumbFile = libs.thumb.picThumbGenerator.returnThumbString(path)
            #files.serveStringFile(thumbFile, path)
            #files.serve(path)
            
        #print 'returnning:',newPath
        return newPath

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': '../../site.log',
                            'log.screen': True,
                            'engine.autoreload_on' : True,
                            'server.socket_port' : 8805,})
    cherrypy.quickstart(Root(), '/')